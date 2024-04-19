from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PromptType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PromptType_USER: _ClassVar[PromptType]
    PromptType_SYSTEM: _ClassVar[PromptType]

class ResponseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ResponseType_COMPLETE: _ClassVar[ResponseType]
    ResponseType_QUEUED: _ClassVar[ResponseType]
PromptType_USER: PromptType
PromptType_SYSTEM: PromptType
ResponseType_COMPLETE: ResponseType
ResponseType_QUEUED: ResponseType

class PromptItem(_message.Message):
    __slots__ = ("Type", "Prompt")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    Type: PromptType
    Prompt: str
    def __init__(self, Type: _Optional[_Union[PromptType, str]] = ..., Prompt: _Optional[str] = ...) -> None: ...

class DiffRequest(_message.Message):
    __slots__ = ("Request", "ResultID")
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    RESULTID_FIELD_NUMBER: _ClassVar[int]
    Request: _containers.RepeatedCompositeFieldContainer[PromptItem]
    ResultID: str
    def __init__(self, Request: _Optional[_Iterable[_Union[PromptItem, _Mapping]]] = ..., ResultID: _Optional[str] = ...) -> None: ...

class DiffResult(_message.Message):
    __slots__ = ("Result", "ResultType", "ResultID")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    RESULTTYPE_FIELD_NUMBER: _ClassVar[int]
    RESULTID_FIELD_NUMBER: _ClassVar[int]
    Result: _containers.RepeatedScalarFieldContainer[str]
    ResultType: ResponseType
    ResultID: str
    def __init__(self, Result: _Optional[_Iterable[str]] = ..., ResultType: _Optional[_Union[ResponseType, str]] = ..., ResultID: _Optional[str] = ...) -> None: ...

class Settings(_message.Message):
    __slots__ = ("Temperature",)
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    Temperature: float
    def __init__(self, Temperature: _Optional[float] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
