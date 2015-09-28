import sys
from _functools import partial
import itertools

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    def b(s):
        return s.encode("latin-1")
    def u(s):
        return s    
    integer_types = int,
    binary_type = bytes
    unichr = chr
    if sys.version_info[1] <= 1:
        def int2byte(i):
            return bytes((i,))
    else:
        # This is about 2x faster than the implementation above on 3.2+
        int2byte = operator.methodcaller("to_bytes", 1, "big")
    byte2int = operator.itemgetter(0)
    iterbytes = iter
    
else:
    integer_types = (int, long)
    binary_type = str
    
    def b(s):
        return s
    # Workaround for standalone backslash
    def u(s):
        return unicode(s.replace(r'\\', r'\\\\'), "unicode_escape")
    unichr = unichr
    int2byte = chr
    def byte2int(bs):
        return ord(bs[0])
    def indexbytes(buf, i):
        return ord(buf[i])
    iterbytes = partial(itertools.imap, ord)
    