#!/bin/sh
python3 -m grpc_tools.protoc --python_out=. --pyi_out=. --grpc_python_out=. -I=. server.proto