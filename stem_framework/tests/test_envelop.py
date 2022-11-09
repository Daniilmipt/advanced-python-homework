import io
import pickle
import mmap
from unittest import TestCase

from stem.envelope import Envelope


class TestEnvelope(TestCase):

    def setUp(self) -> None:
        self.data = b"0123456789"
        self.envelope = Envelope(dict(a=1, b="b"), self.data)

    def test_read(self):
        data = self.envelope.to_bytes()
        envelope = Envelope.from_bytes(data)
        self.assertDictEqual(self.envelope.meta, envelope.meta)
        self.assertEqual(self.envelope.data, envelope.data)

        file_name = 'test.txt'

        with open('../data_files/{}'.format(file_name), 'rb') as file:
            fi = io.FileIO(file.fileno())
            fb = io.BufferedReader(fi)
            a = Envelope.read(fb)
        print(a.meta)
        print(a.data)
        with open('../data_files/test.txt', 'wb') as file:
            a.write_to(file)

        with open('../data_files/test.txt', 'rb') as file:
            print(file.read())
