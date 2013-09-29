import struct
import sys

# Auto-detect system float precision

if sys.float_info.mant_dig == 53:
    float_size = 64
else:
    float_size = 32

################################################################################

class Ext:
    def __init__(self, ext_type, data):
        self.ext_type = ext_type
        self.data = data
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.ext_type == other.ext_type and
                self.data == other.data)
    def __ne__(self, other):
        return not self.__eq__(other)

################################################################################

# Exceptions

class PackException(Exception): pass
class UnpackException(Exception): pass

# Object type not supported for packing
class UnsupportedTypeException(PackException): pass

# Insufficient data to unpack object
class InsufficientDataException(UnpackException): pass
# Non-hashable key encountered during unpacking a map
class KeyNotPrimitiveException(UnpackException): pass
# Duplicate key encountered during unpacking a map
class KeyDuplicateException(UnpackException): pass

################################################################################

def pack_int(x):
    pass

def pack_nil(x):
    pass

def pack_boolean(x):
    pass

def pack_float(x):
    pass

def pack_string(x):
    pass

def pack_binary(x):
    pass

def pack_array(x):
    pass

def pack_map(x):
    pass

def pack_ext(x):
    pass

def packb(x):
    if x is None:
        return pack_nil(x)
    elif isinstance(x, bool):
        return pack_boolean(x)
    elif isinstance(x, int):
        pass
    elif isinstance(x, float):
        pass
    elif isinstance(x, basestring):
        pass
    elif isinstance(x, list):
        pass
    elif isinstance(x, dict):
        pass
    elif isinstance(x, Ext):
        pass
    else:
        raise UnsupportedTypeException("type %s not supported by msgpack" % str(type(x)))

################################################################################


