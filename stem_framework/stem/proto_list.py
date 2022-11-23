from typing import Type, Iterable, Sized, Iterator

GeneratedProtocolMessageType = "GeneratedProtocolMessageType"


class ProtoList(Sized, Iterable):

    def __init__(self, path, proto_class: Type[GeneratedProtocolMessageType]):
        self.path = path
        self.proto_class = proto_class

    def __enter__(self):
        self.file = open(self.path, 'rb')
        n = int.from_bytes(self.file.read(8), "big")
        self.proto_message = self.file.read(n).decode('utf-8')
        return self.proto_message

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.__exit__(exc_type, exc_val, exc_tb)

    def __len__(self) -> int:
        pass

    def __getitem__(self, item):
        pass

    def __iter__(self):
        pass
