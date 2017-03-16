import os
import unittest

from pytsv.pytsv import TsvReader


def get_file(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), "../../", name)


file_doesnt_exist = get_file("data/doesnt_exist.tsv")
file_good = get_file("data/good.tsv")
file_bad = get_file("data/bad.tsv")
file_gzip = get_file("data/good.tsv.gz")


def read_all_file(filename: str):
    with TsvReader(filename=filename) as input_handle:
        for _ in input_handle:
            pass


class TestAll(unittest.TestCase):

    def testOpenNotExists(self):
        self.assertRaises(FileNotFoundError, TsvReader, filename=file_doesnt_exist)

    def testGoodFile(self):
        TsvReader(filename=file_good)

    def testContextManager(self):
        read_all_file(filename=file_good)

    def testBadFile(self):
        self.assertRaises(AssertionError, read_all_file, filename=file_bad)

    def testGzipFile(self):
        read_all_file(filename=file_gzip)