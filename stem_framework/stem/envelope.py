import array
import io
import json
import mmap
import pickle
import sys
from asyncio import StreamReader, StreamWriter
from dataclasses import is_dataclass
from io import RawIOBase, BufferedReader
from json import JSONEncoder
from typing import Optional, Union, Any
from .meta import Meta

Binary = Union[bytes, bytearray, memoryview, array.array, mmap.mmap]


class MetaEncoder(JSONEncoder):
    def default(self, obj: Meta) -> Any:
        if is_dataclass(obj):
            return obj.__dataclass_fields__
        else:
            return json.JSONEncoder.default(self, obj)


class Envelope:
    _MAX_SIZE = 128 * 1024 * 1024  # 128 Mb

    def __init__(self, meta: Meta, data: Optional[Binary] = None):
        self.meta = meta
        if sys.getsizeof(data) >= self._MAX_SIZE:
            file_name = 'data.pickle'
            with open('../data_files/{}'.format(file_name), 'wb') as f:
                pickle.dump(data, f)
            with open('../data_files/{}'.format(file_name), 'rb') as f:
                with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
                    self.data = mmap_obj.read()
        else:
            self.data = data

    def __str__(self):
        return str(self.meta)

    @staticmethod
    def read(input: BufferedReader) -> "Envelope":
        input.read(2)
        type = input.read(4).decode("utf-8")
        meta_type = input.read(2).decode("utf-8")
        meta_length = int.from_bytes(input.read(4), byteorder='big')
        data_length = int.from_bytes(input.read(4), byteorder='big')
        input.read(4)

        meta = json.loads(input.read(meta_length).decode("utf-8").replace("'", "\""))
        data = input.read(data_length)
        return Envelope(meta, data)

    @staticmethod
    def from_bytes(buffer: bytes) -> "Envelope":
        type = buffer[2:6].decode("utf-8")
        meta_type = buffer[6:8].decode("utf-8")
        meta_length = int.from_bytes(buffer[8:12], "big")
        data_length = int.from_bytes(buffer[12:16], "big")
        meta_data = buffer[20:20 + meta_length]
        data = buffer[20 + meta_length:20 + meta_length + data_length]
        meta = json.loads(meta_data.decode('utf8').replace("'", '"'))
        return Envelope(meta, data)

    def to_bytes(self) -> bytes:
        type = b"DF02"
        meta_type = b"DI"  # поставил рандомное значение из 2 байт
        meta = json.dumps(self.meta, cls=MetaEncoder)
        meta = str.encode(meta)
        meta_length = len(meta).to_bytes(4, byteorder='big')
        data_length = len(self.data).to_bytes(4, byteorder='big')
        byte_string = b'#~' + type + meta_type + meta_length + data_length + b'~#\r\n'
        byte_string += meta
        byte_string += self.data
        return byte_string

    def write_to(self, output: RawIOBase):
        type = b"DF02"
        meta_type = b"DI"  # поставил рандомное значение из 2 байт
        meta = json.dumps(self.meta, cls=MetaEncoder)
        meta = str.encode(meta)
        meta_length = len(meta).to_bytes(4, byteorder='big')
        data_length = len(self.data).to_bytes(4, byteorder='big')
        output.write(b'#~' + type + meta_type + meta_length + data_length + b'~#\r\n')
        output.write(meta)
        output.write(self.data)

    @staticmethod
    async def async_read(reader: StreamReader) -> "Envelope":
        pass  # TODO(Assignment 11)

    async def async_write_to(self, writer: StreamWriter):
        pass  # TODO(Assignment 11)
