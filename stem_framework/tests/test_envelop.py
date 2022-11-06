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
        print(data)
        envelope = Envelope.from_bytes(data)
        self.assertDictEqual(self.envelope.meta, envelope.meta)
        self.assertEqual(self.envelope.data, envelope.data)

        file_name = 'data.pickle'

        with open('../data_files/{}'.format(file_name), 'rb') as file:
            fi = io.FileIO(file.fileno())
            fb = io.BufferedReader(fi)
            a = Envelope.read(fb)
        print(a.meta)
        print(a.data)
        with open('test', 'wb') as file:
            print(a.write_to(file))

        with open('test', 'rb') as file:
            print(file.read())
