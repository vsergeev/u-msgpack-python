import umsgpack
import struct
import pytest

single_test_vectors = [
    # None
    [ "nil", None, b"\xc0" ],
    # Booleans
    [ "bool false", False, b"\xc2" ],
    [ "bool true", True, b"\xc3" ],
    # + 7-bit uint
    [ "7-bit uint", 0x00, b"\x00" ],
    [ "7-bit uint", 0x10, b"\x10" ],
    [ "7-bit uint", 0x7f, b"\x7f" ],
    # - 5-bit int
    [ "5-bit sint", -1, b"\xff" ],
    [ "5-bit sint", -16, b"\xf0" ],
    [ "5-bit sint", -32, b"\xe0" ],
    # 8-bit uint
    [ "8-bit uint", 0x80, b"\xcc\x80" ],
    [ "8-bit uint", 0xf0, b"\xcc\xf0" ],
    [ "8-bit uint", 0xff, b"\xcc\xff" ],
    # 16-bit uint
    [ "16-bit uint", 0x100, b"\xcd\x01\x00" ],
    [ "16-bit uint", 0x2000, b"\xcd\x20\x00" ],
    [ "16-bit uint", 0xffff, b"\xcd\xff\xff" ],
    # 32-bit uint
    [ "32-bit uint", 0x10000, b"\xce\x00\x01\x00\x00" ],
    [ "32-bit uint", 0x200000, b"\xce\x00\x20\x00\x00" ],
    [ "32-bit uint", 0xffffffff, b"\xce\xff\xff\xff\xff" ],
    # 64-bit uint
    [ "64-bit uint", 0x100000000, b"\xcf" + b"\x00\x00\x00\x01" + b"\x00\x00\x00\x00" ],
    [ "64-bit uint", 0x200000000000, b"\xcf" + b"\x00\x00\x20\x00" + b"\x00\x00\x00\x00" ],
    [ "64-bit uint", 0xffffffffffffffff, b"\xcf" + b"\xff\xff\xff\xff" + b"\xff\xff\xff\xff" ],
    # 8-bit int
    [ "8-bit int", -33, b"\xd0\xdf" ],
    [ "8-bit int", -100, b"\xd0\x9c" ],
    [ "8-bit int", -128, b"\xd0\x80" ],
    # 16-bit int
    [ "16-bit int", -129, b"\xd1\xff\x7f" ],
    [ "16-bit int", -2000, b"\xd1\xf8\x30" ],
    [ "16-bit int", -32768, b"\xd1\x80\x00" ],
    # 32-bit int
    [ "32-bit int", -32769, b"\xd2\xff\xff\x7f\xff" ],
    [ "32-bit int", -1000000000, b"\xd2\xc4\x65\x36\x00" ],
    [ "32-bit int", -2147483648, b"\xd2\x80\x00\x00\x00" ],
    # 64-bit int
    [ "64-bit int", -2147483649, b"\xd3" + b"\xff\xff\xff\xff" + b"\x7f\xff\xff\xff" ],
    [ "64-bit int", -1000000000000000002, b"\xd3" + b"\xf2\x1f\x49\x4c" + b"\x58\x9b\xff\xfe" ],
    [ "64-bit int", -9223372036854775808, b"\xd3" + b"\x80\x00\x00\x00" + b"\x00\x00\x00\x00" ],
    # 64-bit float
    [ "64-bit float", 0.0, b"\xcb" + b"\x00\x00\x00\x00" + b"\x00\x00\x00\x00" ],
    [ "64-bit float", 2.5, b"\xcb" + b"\x40\x04\x00\x00" + b"\x00\x00\x00\x00" ],
    [ "64-bit float", float(10**35), b"\xcb" + b"\x47\x33\x42\x61" + b"\x72\xc7\x4d\x82" ],
    # Fixstr String
    [ "fix string", "", b"\xa0" ],
    [ "fix string", "a", b"\xa1\x61" ],
    [ "fix string", "abc", b"\xa3\x61\x62\x63" ],
    [ "fix string", "a" * 31, b"\xbf" + b"\x61"*31 ],
    # 8-bit String
    [ "8-bit string", "b" * 32, b"\xd9\x20" + b"b" * 32 ],
    [ "8-bit string", "c" * 100, b"\xd9\x64" + b"c" * 100 ],
    [ "8-bit string", "d" * 255, b"\xd9\xff" + b"d" * 255 ],
    # 16-bit String
    [ "16-bit string", "b" * 256, b"\xda\x01\x00" + b"b" * 256 ],
    [ "16-bit string", "c" * 65535, b"\xda\xff\xff" + b"c" * 65535 ],
    # 32-bit String
    [ "32-bit string", "b" * 65536, b"\xdb\x00\x01\x00\x00" + b"b" * 65536 ],
    # 8-bit Binary
    [ "8-bit binary", b"\x80" * 1, b"\xc4\x01" + b"\x80" * 1 ],
    [ "8-bit binary", b"\x80" * 32, b"\xc4\x20" + b"\x80" * 32 ],
    [ "8-bit binary", b"\x80" * 255, b"\xc4\xff" + b"\x80" * 255 ],
    # 16-bit Binary
    [ "16-bit binary", b"\x80" * 256, b"\xc5\x01\x00" + b"\x80" * 256 ],
    # 32-bit Binary
    [ "32-bit binary", b"\x80" * 65536, b"\xc6\x00\x01\x00\x00" + b"\x80" * 65536 ],
    # Fixext 1
    [ "fixext 1", umsgpack.Ext(0x05, b"\x80"*1), b"\xd4\x05" + b"\x80"*1 ],
    # Fixext 2
    [ "fixext 2", umsgpack.Ext(0x05, b"\x80"*2), b"\xd5\x05" + b"\x80"*2 ],
    # Fixext 4
    [ "fixext 4", umsgpack.Ext(0x05, b"\x80"*4), b"\xd6\x05" + b"\x80"*4 ],
    # Fixext 8
    [ "fixext 8", umsgpack.Ext(0x05, b"\x80"*8), b"\xd7\x05" + b"\x80"*8 ],
    # Fixext 16
    [ "fixext 16", umsgpack.Ext(0x05, b"\x80"*16), b"\xd8\x05" + b"\x80"*16 ],
    # 8-bit Ext
    [ "8-bit ext", umsgpack.Ext(0x05, b"\x80"*255), b"\xc7\xff\x05" + b"\x80"*255 ],
    # 16-bit Ext
    [ "16-bit ext", umsgpack.Ext(0x05, b"\x80"*256), b"\xc8\x01\x00\x05" + b"\x80"*256 ],
    # 32-bit Ext
    [ "32-bit ext", umsgpack.Ext(0x05, b"\x80"*65536), b"\xc9\x00\x01\x00\x00\x05" + b"\x80"*65536 ],
    # Empty Array
    [ "empty array", [], b"\x90" ],
    # Empty Map
    [ "empty map", {}, b"\x80" ],
]

composite_test_vectors = [
    # Fix Array
    [ "fix array", [ 5, "abc", True ], b"\x93\x05\xa3\x61\x62\x63\xc3" ],
    # 16-bit Array
    [ "16-bit array", [ 0x05 ]*16, b"\xdc\x00\x10" + b"\x05"*16 ],
    [ "16-bit array", [ 0x05 ]*65535, b"\xdc\xff\xff" + b"\x05"*65535 ],
    # 32-bit Array
    [ "16-bit array", [ 0x05 ]*65536, b"\xdd\x00\x01\x00\x00" + b"\x05"*65536 ],
    # Fix Map
    [ "fix map", { 1: True, 2: "abc", 3: b"\x80" }, b"\x83\x01\xc3\x02\xa3\x61\x62\x63\x03\xc4\x01\x80" ],
    [ "fix map", { "abc" : 5 }, b"\x81\xa3\x61\x62\x63\x05" ],
    [ "fix map", { b"\x80" : 0xffff }, b"\x81\xc4\x01\x80\xcd\xff\xff" ],
    [ "fix map", { True : None }, b"\x81\xc3\xc0" ],
    # 16-bit Map
    [ "16-bit map", { k: 0x05 for k in range(16) }, b"\xde\x00\x10" + b"".join( [ struct.pack("B", i) + b"\x05" for i in range(16) ] ) ],
    [ "16-bit map", { k: 0x05 for k in range(6000) }, b"\xde\x17\x70" + b"".join([ struct.pack("B", i) + b"\x05" for i in range(128)]) + b"".join([ b"\xcc" + struct.pack("B", i) + b"\x05" for i in range(128, 256)]) + b"".join([ b"\xcd" + struct.pack(">H", i) + b"\x05" for i in range(256, 6000)]) ],
    # Complex Array
    [ "complex array", [ True, 0x01, umsgpack.Ext(0x03, b"foo"), 0xff, { 1: False, 2: "abc" }, b"\x80", [ 1, 2, 3], "abc" ], b"\x98\xc3\x01\xc7\x03\x03\x66\x6f\x6f\xcc\xff\x82\x01\xc2\x02\xa3\x61\x62\x63\xc4\x01\x80\x93\x01\x02\x03\xa3\x61\x62\x63" ],
    # Complex Map
    [  "complex map", { 1 : [{1: 2, 3: 4}, {}], 2: 1, 3: [False, 'def'], 4: {0x100000000: 'a', 0xffffffff: 'b'}}, b"\x84\x01\x92\x82\x01\x02\x03\x04\x80\x02\x01\x03\x92\xc2\xa3\x64\x65\x66\x04\x82\xcf\x00\x00\x00\x01\x00\x00\x00\x00\xa1\x61\xce\xff\xff\xff\xff\xa1\x62" ]
]

pack_exception_test_vectors = [
    # Unsupported type exception
    [ "unsupported type", set([1,2,3]), umsgpack.UnsupportedTypeException ],
    [ "unsupported type", -2**(64-1)-1, umsgpack.UnsupportedTypeException ],
    [ "unsupported type", 2**64, umsgpack.UnsupportedTypeException ],
]

unpack_exception_test_vectors = [
    # Insufficient data to unpack object
    [ "insufficient data 8-bit uint", b"\xcc", umsgpack.InsufficientDataException ],
    [ "insufficient data 16-bit uint", b"\xcd\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data 32-bit uint", b"\xce\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data 64-bit uint", b"\xcf\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data 8-bit int", b"\xd0", umsgpack.InsufficientDataException ],
    [ "insufficient data 16-bit int", b"\xd1\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data 32-bit int", b"\xd2\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data 64-bit int", b"\xd3\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data 32-bit float", b"\xca\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data 64-bit float", b"\xcb\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data fixstr", b"\xa1", umsgpack.InsufficientDataException ],
    [ "insufficient data 8-bit string", b"\xd9", umsgpack.InsufficientDataException ],
    [ "insufficient data 8-bit string", b"\xd9\x01", umsgpack.InsufficientDataException ],
    [ "insufficient data 16-bit string", b"\xda\x01\x00", umsgpack.InsufficientDataException ],
    [ "insufficient data 32-bit string", b"\xdb\x00\x01\x00\x00", umsgpack.InsufficientDataException ],
    [ "insufficient data 8-bit binary", b"\xc4", umsgpack.InsufficientDataException ],
    [ "insufficient data 8-bit binary", b"\xc4\x01", umsgpack.InsufficientDataException ],
    [ "insufficient data 16-bit binary", b"\xc5\x01\x00", umsgpack.InsufficientDataException ],
    [ "insufficient data 32-bit binary", b"\xc6\x00\x01\x00\x00", umsgpack.InsufficientDataException ],
    [ "insufficient data fixarray", b"\x91", umsgpack.InsufficientDataException ],
    [ "insufficient data fixarray", b"\x92\xc2", umsgpack.InsufficientDataException ],
    [ "insufficient data 16-bit array", b"\xdc\x00\xf0\xc2\xc3", umsgpack.InsufficientDataException ],
    [ "insufficient data 32-bit array", b"\xdd\x00\x01\x00\x00\xc2\xc3", umsgpack.InsufficientDataException ],
    [ "insufficient data fixmap", b"\x81", umsgpack.InsufficientDataException ],
    [ "insufficient data fixmap", b"\x82\xc2\xc3", umsgpack.InsufficientDataException ],
    [ "insufficient data 16-bit map", b"\xde\x00\xf0\xc2\xc3", umsgpack.InsufficientDataException ],
    [ "insufficient data 32-bit map", b"\xdf\x00\x01\x00\x00\xc2\xc3", umsgpack.InsufficientDataException ],
    [ "insufficient data fixext 1", b"\xd4", umsgpack.InsufficientDataException ],
    [ "insufficient data fixext 1", b"\xd4\x05", umsgpack.InsufficientDataException ],
    [ "insufficient data fixext 2", b"\xd5\x05\x01", umsgpack.InsufficientDataException ],
    [ "insufficient data fixext 4", b"\xd6\x05\x01\x02\x03", umsgpack.InsufficientDataException ],
    [ "insufficient data fixext 8", b"\xd7\x05\x01\x02\x03", umsgpack.InsufficientDataException ],
    [ "insufficient data fixext 16", b"\xd8\x05\x01\x02\x03", umsgpack.InsufficientDataException ],
    [ "insufficient data ext 8-bit", b"\xc7\x05\x05\x01\x02\x03", umsgpack.InsufficientDataException ],
    [ "insufficient data ext 16-bit", b"\xc8\x01\x00\x05\x01\x02\x03", umsgpack.InsufficientDataException ],
    [ "insufficient data ext 32-bit", b"\xc9\x00\x01\x00\x00\x05\x01\x02\x03", umsgpack.InsufficientDataException ],
    # Non-hashable key { 1 : False, [1,2,3] : True }
    [ "non-primitive key", b"\x82\x01\xc2\x93\x01\x02\x03\xc3", umsgpack.KeyNotPrimitiveException ],
    # Non-hashable key { 1 : True, { 1 : 1 } : False }
    [ "non-primitive key", b"\x82\x01\xc3\x81\x01\x01\xc2", umsgpack.KeyNotPrimitiveException ],
    # Key duplicate { 1 : True, 1 : False }
    [ "duplicate key", b"\x82\x01\xc3\x01\xc2", umsgpack.KeyDuplicateException ],
    # Reserved code (0xc1)
    [ "reserved code", b"\xc1", umsgpack.ReservedCodeException ],
    # Invalid string (non utf-8)
    [ "invalid string", b"\xa1\x80", umsgpack.InvalidStringException ],
]

################################################################################

def test_pack_single():
    for (name, obj, data) in single_test_vectors:
        print("\tTesting %s: object %s" % (name, str(obj) if len(str(obj)) < 24 else str(obj)[0:24] + "..."))
        assert umsgpack.packb(obj) == data

def test_pack_composite():
    for (name, obj, data) in composite_test_vectors:
        print("\tTesting %s: object %s" % (name, str(obj) if len(str(obj)) < 24 else str(obj)[0:24] + "..."))
        assert umsgpack.packb(obj) == data

def test_pack_exceptions():
    for (name, obj, exception) in pack_exception_test_vectors:
        print("\tTesting %s: object %s" % (name, str(obj) if len(str(obj)) < 24 else str(obj)[0:24] + "..."))
        with pytest.raises(exception): umsgpack.packb(obj)

def test_unpack_single():
    for (name, obj, data) in single_test_vectors:
        print("\tTesting %s: object %s" % (name, str(obj) if len(str(obj)) < 24 else str(obj)[0:24] + "..."))
        assert umsgpack.unpackb(data) == obj

def test_unpack_composite():
    for (name, obj, data) in composite_test_vectors:
        print("\tTesting %s: object %s" % (name, str(obj) if len(str(obj)) < 24 else str(obj)[0:24] + "..."))
        assert umsgpack.unpackb(data) == obj

def test_unpack_exceptions():
    for (name, data, exception) in unpack_exception_test_vectors:
        print("\tTesting %s" % name)
        with pytest.raises(exception): umsgpack.unpackb(data)
