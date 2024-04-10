import sys
import argparse
import grpc
from server_pb2_grpc import PeachyServerStub 
from server_pb2 import DiffRequest, DiffResult, PromptItem, PromptType
import server_pb2_pyi_extensions
from ServerCommon import LISTEN_IF_PORT


def makeRequestSingle(line : str) -> PromptItem:
    type = PromptType.PromptType_USER
    if line[0] == "~":
        type = PromptType.PromptType_SYSTEM
        line = line[1:]
    return PromptItem(Type=type, Prompt=line)

def makeRequest(lines) -> DiffRequest:
   req = [makeRequestSingle(i) for i in lines if not i.startswith("#")]
   return DiffRequest(Request=req)

def main(prompt : DiffRequest, ip : str) -> DiffResult:
    ip = f"{ip}:{LISTEN_IF_PORT}"
    with grpc.insecure_channel(ip) as channel:
        proxy = PeachyServerStub(channel)
        print(f"Sending to {ip}: {prompt}")
        result : DiffResult = proxy.Submit( prompt )
        return result

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
    parser.add_argument("ip", help="ip address of server (default to 127.0.0.1)", default='127.0.0.1', nargs='?')
    args = parser.parse_args()
    req = None
    if args.prompt:
        req = makeRequest(parse_arg(args.prompt))
    else:
        req = makeRequest(read_stdin())
    print(str(main(req,args.ip)))