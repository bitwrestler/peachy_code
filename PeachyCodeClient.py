import argparse
import grpc
from server_pb2_grpc import PeachyServerStub 
from server_pb2 import DiffRequest, DiffResult
from ServerCommon import LISTEN_IF_PORT

def main(prompt : str) -> str:
    with grpc.insecure_channel(LISTEN_IF_PORT) as channel:
        proxy = PeachyServerStub(channel)
        result : DiffResult = proxy.Submit( DiffRequest(Request=prompt) )
        return result.Result


if __name__ == "__main__":
    parser = argparse.ArgumentParser("PeachyCodeClient")
    parser.add_argument("prompt", help="code prompt")
    args = parser.parse_args()
    print(main(args[0]))