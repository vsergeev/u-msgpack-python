* Version 2.4.0 - 04/20/2017
    * Add hash special method to Ext class.
    * Add packing option to force floating point precision.
    * Make codebase PEP 8 compliant.
    * Add support for tox automated testing and use it in CI.
    * Contributors
        * Fabien Fleutot, @fab13n - 4c461ed, bdeee20
        * Yuhang (Steven) Wang, @yuhangwang - 5f53bcf
        * Pedro Rodrigues, @medecau - 2f7b667, 456032c, e60bc5e

* Version 2.3.0 - 10/19/2016
    * Add `ext_handlers` option to packing and unpacking functions to support application-defined Ext packing and unpacking hooks.
    * Add `allow_invalid_utf8` option to unpacking functions to allow unpacking of invalid UTF-8 strings.
    * Add hexadecimal prefix to data bytes in string representation of Ext objects.
    * Change version number to semantic versioning.

* Version 2.2 - 09/25/2016
    * Add `use_ordered_dict` option to unpacking functions for unpacking MessagePack maps into the `collections.OrderedDict` type.
    * Add support for `bytearray` type to `unpackb`/`loads` functions.
    * Fix intermittent unit test failures due to non-deterministic packing of dict test vectors.
    * Fix several docstring examples and typos.
    * Add license and unit test to source distribution packaging.
    * Contributors
        * Fairiz 'Fi' Azizi - df59af6
        * INADA Naoki - 23dbf70
        * Jack O'Connor - 7aa0d19

* Version 2.1 - 05/09/2015
    * Improve array and map unpacking performance under Python 2.
    * Add module `__version__` attribute.

* Version 2.0 - 09/29/2014
    * Add streaming serialization and deserialization with `pack`/`dump` and `unpack`/`load`, respectively, for file-like objects.

* Version 1.8 - 09/17/2014
    * Add support for unpacking maps with array container keys. Thanks to ralphjzhang for the report and suggestion (https://github.com/vsergeev/u-msgpack-python/issues/10).

* Version 1.6 - 01/17/2014
    * Fix wide character unicode string serialization. Thanks to cforger for the bug report and fix (https://github.com/vsergeev/u-msgpack-python/issues/8).
    * Add module docstrings.
    * Add module `version` tuple.
    * Add Python standard library style `dumps` and `loads` serialization/deserialization aliases.
    * Rename unpack exceptions `KeyNotPrimitiveException` -> `UnhashableKeyException` and `KeyDuplicateException` -> `DuplicateKeyException`. Add aliases for backwards compatibility.

* Version 1.5 - 12/09/2013
    * Hide internal helper functions from module's exported names.
    * Make unit tests more portable among interpreters (CPython, PyPy).
    * Update documentation for PyPy support.

* Version 1.4 - 11/21/2013
    * Add type checking to Ext class initialization.
    * Add support for Python 2.6.

* Version 1.2 - 10/19/2013
    * Add compatibility mode to support old specification "raw" bytes msgpack type.

* Version 1.0 - 09/29/2013
    * Initial release.
    * Contributors
        * Eugene Ma - 496aaa5
