from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DiffRequest(_message.Message):
    __slots__ = ("Request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    Request: str
    def __init__(self, Request: _Optional[str] = ...) -> None: ...

class DiffResult(_message.Message):
    __slots__ = ("Result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    Result: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, Result: _Optional[_Iterable[str]] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
