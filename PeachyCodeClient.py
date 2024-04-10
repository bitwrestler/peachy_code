import sys
import argparse
import grpc
from server_pb2_grpc import PeachyServerStub 
from server_pb2 import DiffRequest, DiffResult, PromptItem, PromptType
from ServerCommon import LISTEN_IF_PORT


def makeRequestSingle(line : str) -> PromptItem:
    type = PromptType.PromptType_USER
    if line[0] == "~":
        type = PromptType.PromptType_SYSTEM
        line = line[1:]
    return PromptItem(Type=type, Prompt=line)

def makeRequest(lines) -> DiffRequest:
   req = [makeRequestSingle(i) for i in lines]
   return DiffRequest(Request=req)

def main(prompt : DiffRequest) -> str:
    with grpc.insecure_channel(LISTEN_IF_PORT) as channel:
        proxy = PeachyServerStub(channel)
        print(f"Sending: {prompt}")
        result : DiffResult = proxy.Submit( prompt )
        return result.Result

def read_stdin():
    out = []
    for line in sys.stdin:
        if line.rstrip() == ".":
            break
        out.append(line)
    return out

def parse_arg(arg : str):
    return arg.splitlines(keepends=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("PeachyCodeClient")
    parser.add_argument("prompt", help="code prompt", nargs='?')
    args = parser.parse_args()
    req = None
    if args.prompt:
        req = makeRequest(parse_arg(args.prompt))
    else:
        req = makeRequest(read_stdin())
    print(main(req))