import sys
import select
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
   parsedlines = []
   tmpLine = ""
   slurpLine = False
   for aline in lines:
       if len(aline.strip()) == 0:
            continue
       if aline.startswith("#"):
           continue
       if slurpLine:
            tmpLine = tmpLine + aline
       else:
           tmpLine = aline
       if tmpLine.rstrip().endswith("\\"):
           tmpLine = tmpLine.replace("\\\n", "\n")
           slurpLine = True
           continue
       else:
           slurpLine = False
       parsedlines.append(tmpLine)
   req = [makeRequestSingle(i) for i in parsedlines]
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
    while True:
        if not select.select([sys.stdin,],[],[],2.0)[0]:
            break
        line = sys.stdin.readline()
        if not line or line.rstrip() == ".":
            break
        out.append(line)
    return out

def parse_arg(arg : str):
    return arg.splitlines(keepends=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("PeachyCodeClient")
    parser.add_argument("--prompt", help="code prompt", nargs=1)
    parser.add_argument("--ip", help="ip address of server (default to 127.0.0.1)", default='127.0.0.1', nargs=1)
    args = parser.parse_args()
    req = None
    if args.prompt:
        req = makeRequest(parse_arg(args.prompt[0]))
    else:
        req = makeRequest(read_stdin())
    ip = args.ip
    if isinstance(ip, list):
        ip = ip[0]
    #print(req)
    print(str(main(req,ip)))