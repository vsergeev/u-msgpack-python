# Behavior Notes

* Python 2
  * `unicode` type objects are packed into, and unpacked from, the MessagePack
    `string` format
  * `str` type objects are packed into, and unpacked from, the MessagePack
    `binary` format
* Python 3
  * `str` type objects are packed into, and unpacked from, the MessagePack
    `string` format
  * `bytes` type objects are packed into, and unpacked from, the MessagePack
    `binary` format
* The MessagePack string format is strictly decoded with UTF-8 — an exception
  is thrown if the string bytes cannot be decoded into a valid UTF-8 string,
  unless the `allow_invalid_utf8` option is enabled
* The MessagePack array format is unpacked into a Python list, unless it is the
  key of a map, in which case it is unpacked into a Python tuple
* Python tuples and lists are both packed into the MessagePack array format
* Python float types are packed into the MessagePack float32 or float64 format
  depending on the system's `sys.float_info`
* The Python `datetime.datetime` type is packed into, and unpacked from, the
  MessagePack `timestamp` format
    * Note that the Python `datetime.datetime` type only supports microsecond
      resolution, while the MessagePack `timestamp` format supports nanosecond
      resolution. Timestamps with finer than microsecond resolution will lose
      precision during unpacking. Users may override the packing and unpacking
      of the MessagePack `timestamp` format with a custom type for alternate
      behavior.
    * Both naive and aware timestamp are supported. Naive timestamps are packed
      as if they are in the UTC timezone. Timestamps are always unpacked as
      aware `datetime.datetime` objects in the UTC timezone.
* Ext type handlers specified in the optional `ext_handlers` dictionary will
  override `ext_serializable()` classes during packing and unpacking
