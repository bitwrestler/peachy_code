# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cserver.proto\"7\n\nPromptItem\x12\x19\n\x04Type\x18\x01 \x01(\x0e\x32\x0b.PromptType\x12\x0e\n\x06Prompt\x18\x02 \x01(\t\"+\n\x0b\x44iffRequest\x12\x1c\n\x07Request\x18\x01 \x03(\x0b\x32\x0b.PromptItem\"\x1c\n\nDiffResult\x12\x0e\n\x06Result\x18\x01 \x03(\t\"\x07\n\x05\x45mpty*8\n\nPromptType\x12\x13\n\x0fPromptType_USER\x10\x00\x12\x15\n\x11PromptType_SYSTEM\x10\x01\x32p\n\x0cPeachyServer\x12#\n\x06Submit\x12\x0c.DiffRequest\x1a\x0b.DiffResult\x12\x1f\n\x08GPUStats\x12\x06.Empty\x1a\x0b.DiffResult\x12\x1a\n\x08Shutdown\x12\x06.Empty\x1a\x06.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'server_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PROMPTTYPE']._serialized_start=157
  _globals['_PROMPTTYPE']._serialized_end=213
  _globals['_PROMPTITEM']._serialized_start=16
  _globals['_PROMPTITEM']._serialized_end=71
  _globals['_DIFFREQUEST']._serialized_start=73
  _globals['_DIFFREQUEST']._serialized_end=116
  _globals['_DIFFRESULT']._serialized_start=118
  _globals['_DIFFRESULT']._serialized_end=146
  _globals['_EMPTY']._serialized_start=148
  _globals['_EMPTY']._serialized_end=155
  _globals['_PEACHYSERVER']._serialized_start=215
  _globals['_PEACHYSERVER']._serialized_end=327
# @@protoc_insertion_point(module_scope)
