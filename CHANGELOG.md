* Version 1.6
    * Fix wide character unicode string serialization. Thanks to cforger for the bug report and fix (https://github.com/vsergeev/u-msgpack-python/issues/8).
    * Add module docstrings.
    * Add module `version` tuple.
    * Add Python standard library style `dumps` and `loads` serialization/deserialization aliases.
    * Rename unpack exceptions `KeyNotPrimitiveException` -> `UnhashableKeyException` and `KeyDuplicateException` -> `DuplicateKeyException`. Add aliases for backwards compatibility.

* Version 1.5
    * Hide internal helper functions from module's exported names.
    * Make unit tests more portable among interpreters (CPython, PyPy).
    * Update documentation for PyPy support.

* Version 1.4
    * Add type checking to Ext class initialization.
    * Add support for Python 2.6.

* Version 1.2
    * Add compatibility mode to support old specification "raw" bytes msgpack type.

* Version 1.0
    * Initial release.

