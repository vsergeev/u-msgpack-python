from typing import Any, Callable, Protocol, TypeVar

_T = TypeVar("_T")

__version__: str

version: tuple[int, int, int]


def pack(
    obj: Any,
    fp: _SupportsWrite,
    *,
    ext_handlers: dict[type[Any], Callable[[Any], Ext]] | None = None,
    force_float_precision: str = ...,
) -> None: ...


def packb(
    obj: Any,
    *,
    ext_handlers: dict[type[Any], Callable[[Any], Ext]] | None = None,
    force_float_precision: str = ...,
) -> bytes: ...


def dump(
    obj: Any,
    fp: _SupportsWrite,
    *,
    ext_handlers: dict[type[Any], Callable[[Any], Ext]] | None = None,
    force_float_precision: str = ...,
) -> None: ...


def dumps(
    obj: Any,
    *,
    ext_handlers: dict[type[Any], Callable[[Any], Ext]] | None = None,
    force_float_precision: str = ...,
) -> bytes: ...


def unpackb(
    s: bytes | bytearray | memoryview,
    *,
    ext_handlers: dict[int, Callable[[Ext], Any]] | None = None,
    use_ordered_dict: bool = False,
    use_tuple: bool = False,
    allow_invalid_utf8: bool = False,
    max_depth: int | None = None,
) -> Any: ...


def unpack(
    fp: _SupportsRead,
    *,
    ext_handlers: dict[int, Callable[[Ext], Any]] | None = None,
    use_ordered_dict: bool = False,
    use_tuple: bool = False,
    allow_invalid_utf8: bool = False,
    max_depth: int | None = None,
) -> Any: ...


def loads(
    s: bytes | bytearray | memoryview,
    *,
    ext_handlers: dict[int, Callable[[Ext], Any]] | None = None,
    use_ordered_dict: bool = False,
    use_tuple: bool = False,
    allow_invalid_utf8: bool = False,
    max_depth: int | None = None,
) -> Any: ...


def load(
    fp: _SupportsRead,
    *,
    ext_handlers: dict[int, Callable[[Ext], Any]] | None = None,
    use_ordered_dict: bool = False,
    use_tuple: bool = False,
    allow_invalid_utf8: bool = False,
    max_depth: int | None = None,
) -> Any: ...


class _SupportsRead(Protocol):
    def read(self, __size: int) -> bytes: ...


class _SupportsWrite(Protocol):
    def write(self, __data: bytes) -> Any: ...


class Ext:
    type: int
    data: bytes
    def __init__(self, type: int, data: bytes) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...


class InvalidString(bytes): ...


def ext_serializable(ext_type: int) -> Callable[[type[_T]], type[_T]]: ...


class PackException(Exception): ...
class UnpackException(Exception): ...
class UnsupportedTypeException(PackException): ...
class InsufficientDataException(UnpackException): ...
class InvalidStringException(UnpackException): ...
class UnsupportedTimestampException(UnpackException): ...
class ReservedCodeException(UnpackException): ...
class UnhashableKeyException(UnpackException): ...
class DuplicateKeyException(UnpackException): ...
class MaximumDepthException(UnpackException): ...


KeyNotPrimitiveException = UnhashableKeyException
KeyDuplicateException = DuplicateKeyException

compatibility: bool
