* Version 2.8.0 - 05/18/2023
    * Migrate module to package.
    * Migrate documentation to Sphinx.
    * Improve types and formatting in docstrings.
    * Add type stubs.

* Version 2.7.2 - 11/07/2022
    * Fix hex formatting of data bytes in Ext string representation.
    * Contributors
        * Stefan Ring, @Ringdingcoder - 309b1a9

* Version 2.7.1 - 10/24/2020
    * Add Ext type value validation to Ext class and `ext_serializable()` decorator.
    * Change string formatting from `%` to `.format()` throughout codebase.

* Version 2.7.0 - 08/01/2020
    * Add support for packing subclasses of `ext_serializable()` application classes.
    * Contributors
        * Gabe Appleton, @gappleto97 - 620f6ef

* Version 2.6.0 - 04/25/2020
    * Add `use_tuple` option to unpacking functions for unpacking MessagePack arrays into tuples.
    * Add `ext_serializable()` decorator for registration of application classes with Ext types for automatic packing and unpacking.
    * Contributors
        * Gabe Appleton, @gappleto97 - original idea behind 8aa0ee8 in https://github.com/vsergeev/u-msgpack-python/pull/37

* Version 2.5.2 - 08/15/2019
    * Fix DeprecationWarning about using ABCs from 'collections' on Python 3.7.
    * Contributors
        * Gabe Appleton, @gappleto97 - 5ece62a

* Version 2.5.1 - 03/03/2019
    * Fix handling of naive/aware datetime objects when packing the timestamp extension type.
    * Add handling for short reads during file object unpacking.
    * Make Ext base class a new-style object for cleaner inheritance in Python 2.
    * Improve length comparisons and instance checks for minor performance improvement.
    * Contributors
        * Gabe Appleton, @gappleto97 - 28907ba, 76751f3, 7a9b717
        * DisposaBoy, @DisposaBoy - 50b1dd3

* Version 2.5.0 - 03/31/2018
    * Add support for the timestamp extension type.
    * Fix tests on big endian platforms
    * Contributors
        * Sergei Trofimovich, @trofi - 16510e9

* Version 2.4.1 - 04/25/2017
    * Fix module version tuple inconsistency.

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
