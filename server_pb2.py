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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cserver.proto\"\x1e\n\x0b\x44iffRequest\x12\x0f\n\x07Request\x18\x01 \x01(\t\"\x1c\n\nDiffResult\x12\x0e\n\x06Result\x18\x01 \x01(\t23\n\x0cPeachyServer\x12#\n\x06Submit\x12\x0c.DiffRequest\x1a\x0b.DiffResultb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'server_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_DIFFREQUEST']._serialized_start=16
  _globals['_DIFFREQUEST']._serialized_end=46
  _globals['_DIFFRESULT']._serialized_start=48
  _globals['_DIFFRESULT']._serialized_end=76
  _globals['_PEACHYSERVER']._serialized_start=78
  _globals['_PEACHYSERVER']._serialized_end=129
# @@protoc_insertion_point(module_scope)