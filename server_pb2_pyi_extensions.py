from server_pb2 import PromptItem, PromptType , DiffRequest, DiffResult
PromptItem.__str__ = lambda self : f"{PromptType.Name(self.Type)} -> {self.Prompt.rstrip()}"
DiffRequest.__str__ = lambda self :  "\n**BEGIN**" + "\n".join( map(lambda i: str(i), self.Request)) + "**END**\n"
DiffRequest.IsStatusCheck = lambda self: len(self.Request) == 0 and self.ResultID
DiffResult.__str__ = lambda self : "".join(self.Result)