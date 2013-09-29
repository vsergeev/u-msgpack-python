import umsgpack

single_test_vectors = [
    # None
    [ "nil", None, "\xc0" ],
    # Booleans
    [ "bool false", False, "\xc2" ],
    [ "bool true", True, "\xc3" ],
    # + 7-bit uint
    [ "7-bit uint", 0x00, "\x00" ],
    [ "7-bit uint", 0x10, "\x10" ],
    [ "7-bit uint", 0x7f, "\x7f" ],
    # - 5-bit int
    [ "5-bit sint", -1, "\xff" ],
    [ "5-bit sint", -16, "\xf0" ],
    [ "5-bit sint", -32, "\xe0" ],
    # 8-bit uint
    [ "8-bit uint", 0x80, "\xcc\x80" ],
    [ "8-bit uint", 0xf0, "\xcc\xf0" ],
    [ "8-bit uint", 0xff, "\xcc\xff" ],
    # 16-bit uint
    [ "16-bit uint", 0x100, "\xcd\x01\x00" ],
    [ "16-bit uint", 0x2000, "\xcd\x20\x00" ],
    [ "16-bit uint", 0xffff, "\xcd\xff\xff" ],
    # 32-bit uint
    [ "32-bit uint", 0x10000, "\xce\x00\x01\x00\x00" ],
    [ "32-bit uint", 0x200000, "\xce\x00\x20\x00\x00" ],
    [ "32-bit uint", 0xffffffff, "\xce\xff\xff\xff\xff" ],
    # 64-bit uint
    [ "64-bit uint", 0x100000000, "\xcf" + "\x00\x00\x00\x01" + "\x00\x00\x00\x00" ],
    [ "64-bit uint", 0x200000000000, "\xcf" + "\x00\x00\x20\x00" + "\x00\x00\x00\x00" ],
    [ "64-bit uint", 0xffffffffffffffff, "\xcf" + "\xff\xff\xff\xff" + "\xff\xff\xff\xff" ],
    # 8-bit int
    [ "8-bit int", -33, "\xd0\xdf" ],
    [ "8-bit int", -100, "\xd0\x9c" ],
    [ "8-bit int", -128, "\xd0\x80" ],
    # 16-bit int
    [ "16-bit int", -129, "\xd1\xff\x7f" ],
    [ "16-bit int", -2000, "\xd1\xf8\x30" ],
    [ "16-bit int", -32768, "\xd1\x80\x00" ],
    # 32-bit int
    [ "32-bit int", -32769, "\xd2\xff\xff\x7f\xff" ],
    [ "32-bit int", -1000000000, "\xd2\xc4\x65\x36\x00" ],
    [ "32-bit int", -2147483648, "\xd2\x80\x00\x00\x00" ],
    # 64-bit int
    [ "64-bit int", -2147483649, "\xd3" + "\xff\xff\xff\xff" + "\x7f\xff\xff\xff" ],
    [ "64-bit int", -1000000000000000002, "\xd3" + "\xf2\x1f\x49\x4c" + "\x58\x9b\xff\xfe" ],
    [ "64-bit int", -9223372036854775808, "\xd3" + "\x80\x00\x00\x00" + "\x00\x00\x00\x00" ],
    # 64-bit float
    [ "64-bit float", 0.0, "\xcb" + "\x00\x00\x00\x00" + "\x00\x00\x00\x00" ],
    [ "64-bit float", 2.5, "\xcb" + "\x40\x04\x00\x00" + "\x00\x00\x00\x00" ],
    [ "64-bit float", float(10**35), "\xcb" + "\x47\x33\x42\x61" + "\x72\xc7\x4d\x82" ],
    # Fixstr String
    [ "fix string", "", "\xa0" ],
    [ "fix string", "a", "\xa1\x61" ],
    [ "fix string", "abc", "\xa3\x61\x62\x63" ],
    [ "fix string", "a" * 31, "\xbf" + "\x61"*31 ],
    # 8-bit String
    [ "8-bit string", "b" * 32, "\xd9\x20" + "b" * 32 ],
    [ "8-bit string", "c" * 100, "\xd9\x64" + "c" * 100 ],
    [ "8-bit string", "d" * 255, "\xd9\xff" + "d" * 255 ],
    # 16-bit String
    [ "16-bit string", "b" * 256, "\xda\x01\x00" + "b" * 256 ],
    [ "16-bit string", "c" * 65535, "\xda\xff\xff" + "c" * 65535 ],
    # 32-bit String
    [ "32-bit string", "b" * 65536, "\xdb\x00\x01\x00\x00" + "b" * 65536 ],
    # 8-bit Binary
    [ "8-bit binary", "\x80" * 1, "\xc4\x01" + "\x80" * 1 ],
    [ "8-bit binary", "\x80" * 32, "\xc4\x20" + "\x80" * 32 ],
    [ "8-bit binary", "\x80" * 255, "\xc4\xff" + "\x80" * 255 ],
    # 16-bit Binary
    [ "16-bit binary", "\x80" * 256, "\xc5\x01\x00" + "\x80" * 256 ],
    # 32-bit Binary
    [ "32-bit binary", "\x80" * 65536, "\xc6\x00\x01\x00\x00" + "\x80" * 65536 ],
    # Fixext 1
    [ "fixext 1", umsgpack.Ext(0x05, "\x80"*1), "\xd4\x05" + "\x80"*1 ],
    # Fixext 2
    [ "fixext 2", umsgpack.Ext(0x05, "\x80"*2), "\xd5\x05" + "\x80"*2 ],
    # Fixext 4
    [ "fixext 4", umsgpack.Ext(0x05, "\x80"*4), "\xd6\x05" + "\x80"*4 ],
    # Fixext 8
    [ "fixext 8", umsgpack.Ext(0x05, "\x80"*8), "\xd7\x05" + "\x80"*8 ],
    # Fixext 16
    [ "fixext 16", umsgpack.Ext(0x05, "\x80"*16), "\xd8\x05" + "\x80"*16 ],
    # 8-bit Ext
    [ "8-bit ext", umsgpack.Ext(0x05, "\x80"*255), "\xc7\xff\x05" + "\x80"*255 ],
    # 16-bit Ext
    [ "16-bit ext", umsgpack.Ext(0x05, "\x80"*256), "\xc8\x01\x00\x05" + "\x80"*256 ],
    # 32-bit Ext
    [ "32-bit ext", umsgpack.Ext(0x05, "\x80"*65536), "\xc9\x00\x01\x00\x00\x05" + "\x80"*65536 ],
    # Empty Array
    [ "empty array", [], "\x90" ],
    # Empty Map
    [ "empty map", {}, "\x80" ],
]

composite_test_vectors = [
    # Fix Array
    [ "fix array", [ 5, "abc", True ], "\x93\x05\xa3\x61\x62\x63\xc3" ],
    # 16-bit Array
    [ "16-bit array", [ 0x05 ]*16, "\xdc\x00\x10" + "\x05"*16 ],
    [ "16-bit array", [ 0x05 ]*65535, "\xdc\xff\xff" + "\x05"*65535 ],
    # 32-bit Array
    [ "16-bit array", [ 0x05 ]*65536, "\xdd\x00\x01\x00\x00" + "\x05"*65536 ],
    # Fix Map
    [ "fix map", { 1: True, 2: "abc", 3: "\x80" }, "\x83\x01\xc3\x02\xa3\x61\x62\x63\x03\xc4\x01\x80" ],
    # 16-bit Map
    [ "16-bit map", { k: 0x05 for k in range(16) }, "\xde\x00\x10" + "".join( [ chr(i)+"\x05" for i in range(16) ] ) ],
    [ "16-bit map", { k: 0x05 for k in range(6000) }, "\xde\x17\x70" + "".join([ chr(i)+"\x05" for i in range(128)]) + "".join(["\xcc"+chr(i)+"\x05" for i in range(128, 256)]) + "".join(["\xcd"+chr(i >> 8)+chr(i & 0xff)+"\x05" for i in range(256, 6000)]) ],
    # Complex Array
    [ "complex array", [ True, 0x01, umsgpack.Ext(0x03, "foo"), 0xff, { 1: False, "def": "abc" }, "\x80", [ 1, 2, 3], "abc" ], "\x98\xc3\x01\xc7\x03\x03\x66\x6f\x6f\xcc\xff\x82\x01\xc2\xa3\x64\x65\x66\xa3\x61\x62\x63\xc4\x01\x80\x93\x01\x02\x03\xa3\x61\x62\x63" ],
    # Complex Map
    [  "complex map", {'a': [{1: 2, 3: 4}, {}], True: 1, 5: [False, 'def'], '\x80': {0x100000000: 'a', 0xffffffff: 'b'}}, "\x84\xa1\x61\x92\x82\x01\x02\x03\x04\x80\xc3\x01\x05\x92\xc2\xa3\x64\x65\x66\xc4\x01\x80\x82\xcf\x00\x00\x00\x01\x00\x00\x00\x00\xa1\x61\xce\xff\xff\xff\xff\xa1\x62" ]
]

pack_exception_test_vectors = [
    # Unsupported type exception
    [ "unsupported type", set([1,2,3]), umsgpack.UnsupportedTypeException ],
    [ "unsupported type", -2**(64-1)-1, umsgpack.UnsupportedTypeException ],
    [ "unsupported type", 2**64, umsgpack.UnsupportedTypeException ],
]

unpack_exception_test_vectors = [
    # Insufficient data to unpack object
    [ "insufficient data 8-bit uint", "\xcc", umsgpack.InsufficientDataException ],
    [ "insufficient data 16-bit uint", "\xcd\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data 32-bit uint", "\xce\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data 64-bit uint", "\xcf\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data 8-bit int", "\xd0", umsgpack.InsufficientDataException ],
    [ "insufficient data 16-bit int", "\xd1\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data 32-bit int", "\xd2\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data 64-bit int", "\xd3\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data 32-bit float", "\xca\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data 64-bit float", "\xcb\xff", umsgpack.InsufficientDataException ],
    [ "insufficient data fixstr", "\xa1", umsgpack.InsufficientDataException ],
    [ "insufficient data 8-bit string", "\xd9", umsgpack.InsufficientDataException ],
    [ "insufficient data 8-bit string", "\xd9\x01", umsgpack.InsufficientDataException ],
    [ "insufficient data 16-bit string", "\xda\x01\x00", umsgpack.InsufficientDataException ],
    [ "insufficient data 32-bit string", "\xdb\x00\x01\x00\x00", umsgpack.InsufficientDataException ],
    [ "insufficient data 8-bit binary", "\xc4", umsgpack.InsufficientDataException ],
    [ "insufficient data 8-bit binary", "\xc4\x01", umsgpack.InsufficientDataException ],
    [ "insufficient data 16-bit binary", "\xc5\x01\x00", umsgpack.InsufficientDataException ],
    [ "insufficient data 32-bit binary", "\xc6\x00\x01\x00\x00", umsgpack.InsufficientDataException ],
    [ "insufficient data fixarray", "\x91", umsgpack.InsufficientDataException ],
    [ "insufficient data fixarray", "\x92\xc2", umsgpack.InsufficientDataException ],
    [ "insufficient data 16-bit array", "\xdc\x00\xf0\xc2\xc3", umsgpack.InsufficientDataException ],
    [ "insufficient data 32-bit array", "\xdd\x00\x01\x00\x00\xc2\xc3", umsgpack.InsufficientDataException ],
    [ "insufficient data fixmap", "\x81", umsgpack.InsufficientDataException ],
    [ "insufficient data fixmap", "\x82\xc2\xc3", umsgpack.InsufficientDataException ],
    [ "insufficient data 16-bit map", "\xde\x00\xf0\xc2\xc3", umsgpack.InsufficientDataException ],
    [ "insufficient data 32-bit map", "\xdf\x00\x01\x00\x00\xc2\xc3", umsgpack.InsufficientDataException ],
    [ "insufficient data fixext 1", "\xd4", umsgpack.InsufficientDataException ],
    [ "insufficient data fixext 1", "\xd4\x05", umsgpack.InsufficientDataException ],
    [ "insufficient data fixext 2", "\xd5\x05\x01", umsgpack.InsufficientDataException ],
    [ "insufficient data fixext 4", "\xd6\x05\x01\x02\x03", umsgpack.InsufficientDataException ],
    [ "insufficient data fixext 8", "\xd7\x05\x01\x02\x03", umsgpack.InsufficientDataException ],
    [ "insufficient data fixext 16", "\xd8\x05\x01\x02\x03", umsgpack.InsufficientDataException ],
    [ "insufficient data ext 8-bit", "\xc7\x05\x05\x01\x02\x03", umsgpack.InsufficientDataException ],
    [ "insufficient data ext 16-bit", "\xc8\x01\x00\x05\x01\x02\x03", umsgpack.InsufficientDataException ],
    [ "insufficient data ext 32-bit", "\xc9\x00\x01\x00\x00\x05\x01\x02\x03", umsgpack.InsufficientDataException ],
    # Non-hashable key { 1 : False, [1,2,3] : True }
    [ "non-primitive key", "\x82\x01\xc2\x93\x01\x02\x03\xc3", umsgpack.KeyNotPrimitiveException ],
    # Non-hashable key { 1 : True, { 1 : 1 } : False }
    [ "non-primitive key", "\x82\x01\xc3\x81\x01\x01\xc2", umsgpack.KeyNotPrimitiveException ],
    # Key duplicate { 1 : True, 1 : False }
    [ "duplicate key", "\x82\x01\xc3\x01\xc2", umsgpack.KeyDuplicateException ],
    # Reserved code (0xc1)
    [ "reserved code", "\xc1", umsgpack.ReservedCodeException ]
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
        try:
            _ = umsgpack.packb(obj)
        except Exception as e:
            assert isinstance(e, exception)

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
        try:
            _ = umsgpack.unpackb(data)
        except Exception as e:
            assert isinstance(e, exception)

def test_validate_single():
    for (name, obj, data) in single_test_vectors:
        print("\tTesting %s: object %s" % (name, str(obj) if len(str(obj)) < 24 else str(obj)[0:24] + "..."))
        assert umsgpack.validate(data)

def test_validate_composite():
    for (name, obj, data) in composite_test_vectors:
        print("\tTesting %s: object %s" % (name, str(obj) if len(str(obj)) < 24 else str(obj)[0:24] + "..."))
        assert umsgpack.validate(data)

def test_validate_exceptions():
    for (name, data, exception) in unpack_exception_test_vectors:
        print("\tTesting %s" % name)
        if exception == umsgpack.InsufficientDataException:
            assert umsgpack.validate(data) == False
        else:
            try:
                _ = umsgpack.validate(data)
            except Exception as e:
                assert isinstance(e, exception)

