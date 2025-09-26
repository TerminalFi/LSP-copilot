import sys
from _typeshed import Incomplete
from io import BytesIO as BytesIO, StringIO

PY2: Incomplete
PYPY: Incomplete
unichr = chr
range_type = range
text_type = str
string_types: Incomplete
integer_types: Incomplete
iterkeys: Incomplete
itervalues: Incomplete
iteritems: Incomplete
NativeStringIO = StringIO

def reraise(tp, value, tb: Incomplete | None = None) -> None: ...
ifilter = filter
imap = map
izip = zip
intern = sys.intern
implements_iterator: Incomplete
implements_to_string: Incomplete
encode_filename: Incomplete

def with_metaclass(meta, *bases): ...
