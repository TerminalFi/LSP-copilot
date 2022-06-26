
import json


class Spec(object):
    """
    This class wraps methods that create JSON-RPC 2.0 compatible string representations of
    request, response and error objects. All methods are class members, so you might never want to
    create an instance of this class, but rather use the methods directly:
    .. code-block:: python
        Spec.request("my_method", 18)  # the id is optional
        # => '{"jsonrpc":"2.0","method":"my_method","id": 18}'
        Spec.response(18, "some_result")
        # => '{"jsonrpc":"2.0","id":18,"result":"some_result"}'
        Spec.error(18, -32603)
        # => '{"jsonrpc":"2.0","id":18,"error":{"code":-32603,"message":"Internal error"}}'
    """

    @classmethod
    def check_id(cls, id, allow_empty=False):
        """
        Value check for *id* entries. When *allow_empty* is *True*, *id* is allowed to be *None*.
        Raises a *TypeError* when *id* is neither an integer nor a string.
        """
        if (id is not None or not allow_empty) and not isinstance(id, (int, str)):
            raise TypeError(
                "id must be an integer or string, got {} ({})".format(id, type(id)))

    @classmethod
    def check_method(cls, method):
        """
        Value check for *method* entries. Raises a *TypeError* when *method* is not a string.
        """
        if not isinstance(method, str):
            raise TypeError(
                "method must be a string, got {} ({})".format(method, type(method)))

    @classmethod
    def check_code(cls, code):
        """
        Value check for *code* entries. Raises a *TypeError* when *code* is not an integer, or a
        *KeyError* when there is no :py:class:`RPCError` subclass registered for that *code*.
        """
        if not isinstance(code, int):
            raise TypeError(
                "code must be an integer, got {} ({})".format(id, type(id)))

        if not get_error(code):
            raise ValueError(
                "unknown code, got {} ({})".format(code, type(code)))

    @classmethod
    def request(cls, method, id=None, params=None):
        """
        Creates the string representation of a request that calls *method* with optional *params*
        which are encoded by ``json.dumps``. When *id* is *None*, the request is considered a
        notification.
        """
        try:
            cls.check_method(method)
            cls.check_id(id, allow_empty=True)
        except Exception as e:
            raise RPCInvalidRequest(str(e))

        req = {
            'jsonrpc': '2.0',
            'method': method,
            'id': '{}'.format(id),
            'params': params
        }

        # # start building the request string
        # req = "{{\"jsonrpc\":\"2.0\", \"method\":\"{}\"".format(method)

        # # add the id when given
        # if id is not None:
        #     # encode string ids
        #     if isinstance(id, str):
        #         id = json.dumps(id)
        #     req += ",\"id\":{}".format(id)

        # # add parameters when given
        # if params is not None:
        #     try:
        #         req += ",\"params\":{}".format(json.dumps(params))
        #     except Exception as e:
        #         raise RPCParseError(str(e))

        # # end the request string
        # req += "}"

        return req

    @classmethod
    def response(cls, id, result):
        """
        Creates the string representation of a respone that was triggered by a request with *id*.
        A *result* is required, even if it is *None*.
        """
        try:
            cls.check_id(id)
        except Exception as e:
            raise RPCInvalidRequest(str(e))

        # encode string ids
        if isinstance(id, str):
            id = json.dumps(id)

        res = {
            'jsonrpc': '2.0',
            'id': '{}'.format(id),
            'result': result
        }

        # build the response string
        # try:
        #     res = "{{\"jsonrpc\":\"2.0\",\"id\":{},\"result\":{}}}".format(
        #         id, json.dumps(result))
        # except Exception as e:
        #     raise RPCParseError(str(e))

        return res

    @classmethod
    def error(cls, id, code, data=None):
        """
        Creates the string representation of an error that occured while processing a request with
        *id*. *code* must lead to a registered :py:class:`RPCError`. *data* might contain
        additional, detailed error information and is encoded by ``json.dumps`` when set.
        """
        try:
            cls.check_id(id)
            cls.check_code(code)
        except Exception as e:
            raise RPCInvalidRequest(str(e))

        title = ''
        message = get_error(code)
        if message is not None:
            title = message.title
        else:
            title = 'UNKNOWN'
        # build the inner error data
        # err_data = "{{\"code\":{},\"message\":\"{}\"".format(code, title)

        err = {
            'jsonrpc': '2.0',
            'id': '{}'.format(id),
            'error': {
                'code': '',
                'message': '',
                'data': {
                    'code': code,
                    'message': title
                }
            }
        }

        # # insert data when given
        # if data is not None:
        #     try:
        #         err_data += ",\"data\":{}}}".format(json.dumps(data))
        #     except Exception as e:
        #         raise RPCParseError(str(e))
        # else:
        #     err_data += "}"

        # # encode string ids
        # if isinstance(id, str):
        #     id = json.dumps(id)

        # # start building the error string
        # err = "{{\"jsonrpc\":\"2.0\",\"id\":{},\"error\":{}}}".format(
        #     id, err_data)

        return err


class RPCError(Exception):

    """
    Base class for RPC errors.
    .. py:attribute:: message
       The message of this error, i.e., ``"<title> (<code>)[, data: <data>]"``.
    .. py:attribute:: data
       Additional data of this error. Setting the data attribute will also change the message
       attribute.
    """

    def __init__(self, data=None):
        # build the error message
        message = "{} ({})".format(self.title, self.code)
        if data is not None:
            message += ", data: {}".format(data)
        self.message = message

        super(RPCError, self).__init__(message)

        self.data = data

    def __str__(self):
        return self.message


error_map_distinct = {}
error_map_range = {}


def is_range(code):
    return (
        isinstance(code, tuple) and
        len(code) == 2 and
        all(isinstance(i, int) for i in code) and
        code[0] < code[1]
    )


def register_error(cls):
    """
    Decorator that registers a new RPC error derived from :py:class:`RPCError`. The purpose of
    error registration is to have a mapping of error codes/code ranges to error classes for faster
    lookups during error creation.
    .. code-block:: python
       @register_error
       class MyCustomRPCError(RPCError):
           code = ...
           title = "My custom error"
    """
    # it would be much cleaner to add a meta class to RPCError as a registry for codes
    # but in CPython 2 exceptions aren't types, so simply provide a registry mechanism here
    if not issubclass(cls, RPCError):
        raise TypeError("'{}' is not a subclass of RPCError".format(cls))

    code = cls.code

    if isinstance(code, int):
        error_map = error_map_distinct
    elif is_range(code):
        error_map = error_map_range
    else:
        raise TypeError("invalid RPC error code {}".format(code))

    if code in error_map:
        raise AttributeError("duplicate RPC error code {}".format(code))

    error_map[code] = cls

    return cls


def get_error(code):
    """
    Returns the RPC error class that was previously registered to *code*. *None* is returned when no
    class could be found.
    """
    if code in error_map_distinct:
        return error_map_distinct[code]

    for (lower, upper), cls in error_map_range.items():
        if lower <= code <= upper:
            return cls

    return None


@register_error
class RPCParseError(RPCError):

    code = -32700
    title = "Parse error"


@register_error
class RPCInvalidRequest(RPCError):

    code = -32600
    title = "Invalid Request"


@register_error
class RPCMethodNotFound(RPCError):

    code = -32601
    title = "Method not found"


@register_error
class RPCInvalidParams(RPCError):

    code = -32602
    title = "Invalid params"


@register_error
class RPCInternalError(RPCError):

    code = -32603
    title = "Internal error"


@register_error
class RPCServerError(RPCError):

    code = (-32099, -32000)
    title = "Server error"
