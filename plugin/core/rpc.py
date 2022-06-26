# Heavily inspired by https://github.com/sublimelsp/LSP/blob/main/plugin/core/transports.py

from .types import TCP_CONNECT_TIMEOUT
from .types import TransportConfig
from .typing import Dict
from .typing import Any
from .typing import Optional
from .typing import IO
from .typing import Protocol
from .typing import Generic
from .typing import List
from .typing import Callable
from .typing import Tuple
from .typing import TypeVar
from .typing import Union
from .spec import Spec
from contextlib import closing
from queue import Queue
import json
import os
import socket
import subprocess
import threading
import time
import weakref


T = TypeVar('T')
T_contra = TypeVar('T_contra', contravariant=True)


def exception_log(a, b):
    print(a, b)


def debug(a):
    print(a)


class StopLoopError(Exception):
    pass


class Transport(Generic[T]):

    def send(self, payload: T) -> None:
        raise NotImplementedError()

    def send_json_rpc(self, method: str, params: Dict) -> None:
        raise NotImplementedError()

    def close(self) -> None:
        raise NotImplementedError()


class TransportCallbacks(Protocol[T_contra]):

    def on_transport_close(self, exit_code: int, exception: Optional[Exception]) -> None:
        ...

    def on_payload(self, method: str, payload: T_contra) -> None:
        ...

    def on_stderr_message(self, message: str) -> None:
        ...


class AbstractProcessor(Generic[T]):

    def write_data(self, writer: IO[bytes], data: T) -> None:
        raise NotImplementedError()

    def read_data(self, reader: IO[bytes]) -> Optional[T]:
        raise NotImplementedError()


class JsonRpcProcessor(AbstractProcessor[Dict[str, Any]]):

    def write_data(self, writer: IO[bytes], data: Dict[str, Any]) -> None:
        body = self._encode(data)
        writer.writelines(
            ("Content-Length: {}\r\n\r\n".format(len(body)).encode('ascii'), body))

    def read_data(self, reader: IO[bytes]) -> Optional[Dict[str, Any]]:
        line = reader.readline().decode('utf-8')
        if len(line) == 0:
            return None

        if line == 'Content-Length: 232\r\n' or line == '\r\n':
            return None

        body = line.split('Content-Length')
        try:
            return self._decode(body[0])
        except Exception as ex:
            exception_log("JSON decode error", ex)
            return None

    @staticmethod
    def _encode(data: Dict[str, Any]) -> bytes:
        return json.dumps(
            data,
            ensure_ascii=False,
            sort_keys=False,
            check_circular=False,
            separators=(',', ':')
        ).encode('utf-8')

    @staticmethod
    def _decode(message: str) -> Dict[str, Any]:
        return json.loads(message)


class ProcessTransport(Transport[T]):

    def __init__(self, name: str, process: subprocess.Popen, reader: IO[bytes],
                 writer: IO[bytes], stderr: Optional[IO[bytes]], processor: AbstractProcessor[T],
                 callback_object: TransportCallbacks[T]) -> None:
        self._i = -1
        self._methods = {}
        self._closed = False
        self._process = process
        self._reader = reader
        self._writer = writer
        self._stderr = stderr
        self._processor = processor
        self._reader_thread = threading.Thread(
            target=self._read_loop, name='{}-reader'.format(name))
        self._writer_thread = threading.Thread(
            target=self._write_loop, name='{}-writer'.format(name))
        self._stderr_thread = threading.Thread(
            target=self._stderr_loop, name='{}-stderr'.format(name))
        self._callback_object = weakref.ref(callback_object)
        self._send_queue = Queue(0)  # type: Queue[Union[T, None]]
        self._reader_thread.start()
        self._writer_thread.start()
        self._stderr_thread.start()

    def send_json_rpc(self, method: str, params, callback: Any = None) -> None:
        self._i += 1
        self._methods[self._i] = {
            'method': method,
            'callback': callback if callback is not None else None
            }
        req = Spec.request(method=method, id=self._i, params=params)
        self._send_queue.put_nowait(req)

    def send(self, payload: T) -> None:
        self._send_queue.put_nowait(payload)

    def close(self) -> None:
        if not self._closed:
            self._send_queue.put_nowait(None)
            self._closed = True

    def _join_thread(self, t: threading.Thread) -> None:
        if t.ident == threading.current_thread().ident:
            return
        try:
            t.join(2)
        except TimeoutError as ex:
            exception_log("failed to join {} thread".format(t.name), ex)

    def __del__(self) -> None:
        self.close()
        self._join_thread(self._writer_thread)
        self._join_thread(self._reader_thread)
        self._join_thread(self._stderr_thread)

    def _read_loop(self) -> None:
        try:
            while self._reader:
                payload = self._processor.read_data(self._reader)
                if payload is None:
                    continue
                obj = dict(**payload)
                req_id = int(obj.get("id", -1))
                details = self._methods.get(req_id, None)
                method = ''
                callback = None # type: Any
                if details is not None:
                    method = details.get('method', None)
                    callback = details.get('callback', None)

                if method is None:
                    # try seeing if the response has a method
                    method = obj.get('method', None)
                if method is None:
                    method = 'unspecified'

                print('<--- Server:Copilot\t{}({})\t{}'.format(method, req_id, obj))

                def invoke(method: str, payload: T) -> None:
                    if self._closed:
                        return
                    callback_object = self._callback_object()
                    if callback_object:
                        callback_object.on_payload(method, payload)

                if callback is None:
                    invoke(method, payload)
                else:
                    callback(payload)
                try:
                    del self._methods[req_id]
                except:
                    pass
                # sublime.set_timeout_async(partial(invoke, payload))
        except (AttributeError, BrokenPipeError, StopLoopError):
            pass
        except Exception as ex:
            exception_log("Unexpected exception", ex)
        self._send_queue.put_nowait(None)

    def _end(self, exception: Optional[Exception]) -> None:
        exit_code = 0
        if not exception:
            try:
                # Allow the process to stop itself.
                exit_code = self._process.wait(1)
            except (AttributeError, ProcessLookupError, subprocess.TimeoutExpired):
                pass
        if self._process.poll() is None:
            try:
                # The process didn't stop itself. Terminate!
                self._process.kill()
                # still wait for the process to die, or zombie processes might be the result
                # Ignore the exit code in this case, it's going to be something non-zero because we sent SIGKILL.
                self._process.wait()
            except (AttributeError, ProcessLookupError):
                pass
            except Exception as ex:
                exception = ex  # TODO: Old captured exception is overwritten

        def invoke() -> None:
            callback_object = self._callback_object()
            if callback_object:
                callback_object.on_transport_close(exit_code, exception)

        # sublime.set_timeout_async(invoke)
        self.close()

    def _write_loop(self) -> None:
        exception = None  # type: Optional[Exception]
        try:
            while self._writer:
                d = self._send_queue.get()
                if d is None:
                    continue
                obj = dict(**d)
                print('---> Client:Copilot\t{}({})\t{}'.format(obj.get("method", "UNKNOWN"), obj.get("id", "unspecified"), obj))
                # print('breaking')
                # break
                self._processor.write_data(self._writer, d)
                self._writer.flush()
        except (BrokenPipeError, AttributeError):
            pass
        except Exception as ex:
            exception = ex
        self._end(exception)

    def _stderr_loop(self) -> None:
        try:
            while self._stderr:
                if self._closed:
                    # None message already posted, just return
                    return
                message = self._stderr.readline().decode('utf-8', 'replace')
                if message == '':
                    continue
                callback_object = self._callback_object()
                if callback_object:
                    callback_object.on_stderr_message(message.rstrip())
                else:
                    break
        except (BrokenPipeError, AttributeError):
            pass
        except Exception as ex:
            exception_log('unexpected exception type in stderr loop', ex)
        self._send_queue.put_nowait(None)


# Can be a singleton since it doesn't hold any state.
json_rpc_processor = JsonRpcProcessor()


def create_transport(config: TransportConfig, cwd: Optional[str],
                     callback_object: TransportCallbacks) -> Transport[Dict[str, Any]]:
    stdout = subprocess.PIPE
    stdin = subprocess.PIPE
    startupinfo = _fixup_startup_args(config.command)
    process = None  # type: Optional[subprocess.Popen]

    def start_subprocess() -> subprocess.Popen:
        return _start_subprocess(config.command, stdin, stdout, subprocess.PIPE, startupinfo, config.env, cwd)

    process = start_subprocess()
    reader = process.stdout  # type: ignore
    writer = process.stdin  # type: ignore
    if not reader or not writer:
        raise RuntimeError(
            'Failed initializing transport: reader: {}, writer: {}'.format(reader, writer))
    return ProcessTransport(config.name, process, reader, writer, process.stderr, json_rpc_processor,
                            callback_object)


_subprocesses = weakref.WeakSet()  # type: weakref.WeakSet[subprocess.Popen]


def kill_all_subprocesses() -> None:
    global _subprocesses
    subprocesses = list(_subprocesses)
    for p in subprocesses:
        try:
            p.kill()
        except Exception:
            pass
    for p in subprocesses:
        try:
            p.wait()
        except Exception:
            pass


def _fixup_startup_args(args: List[str]) -> Any:
    startupinfo = None
    # if sublime.platform() == "windows":
    #     startupinfo = subprocess.STARTUPINFO()  # type: ignore
    #     startupinfo.dwFlags |= subprocess.SW_HIDE | subprocess.STARTF_USESHOWWINDOW  # type: ignore
    #     executable_arg = args[0]
    #     _, ext = os.path.splitext(executable_arg)
    #     if len(ext) < 1:
    #         path_to_executable = shutil.which(executable_arg)
    #         # what extensions should we append so CreateProcess can find it?
    #         # node has .cmd
    #         # dart has .bat
    #         # python has .exe wrappers - not needed
    #         for extension in ['.cmd', '.bat']:
    #             if path_to_executable and path_to_executable.lower().endswith(extension):
    #                 args[0] = executable_arg + extension
    #                 break
    return startupinfo


def _start_subprocess(
    args: List[str],
    stdin: int,
    stdout: int,
    stderr: int,
    startupinfo: Any,
    env: Dict[str, str],
    cwd: Optional[str]
) -> subprocess.Popen:
    debug("starting {} in {}".format(args, cwd if cwd else os.getcwd()))
    process = subprocess.Popen(
        args=args,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        startupinfo=startupinfo,
        # env=env,
        # cwd=cwd
    )
    _subprocesses.add(process)
    return process
