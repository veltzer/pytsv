"""
test_all.py
"""

import gzip
import os
import tempfile
import unittest

import pytest

from pytsv.core import TsvReader, TsvWriter


def get_file(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), "../../", name)


file_doesnt_exist = get_file("data/doesnt_exist.tsv")
file_good = get_file("data/good.tsv")
file_bad = get_file("data/bad.tsv")
file_gzip = get_file("data/good.tsv.gz")


def read_all_file(filename: str) -> None:
    with TsvReader(filename=filename) as input_handle:
        for _ in input_handle:
            pass


class TestAll(unittest.TestCase):

    def test_open_not_exists(self) -> None:
        with pytest.raises(FileNotFoundError):
            TsvReader(filename=file_doesnt_exist)

    def test_good_file(self) -> None:
        g = TsvReader(filename=file_good)
        g.close()

    def test_context_manager(self) -> None:
        read_all_file(filename=file_good)

    def test_bad_file(self) -> None:
        with pytest.raises(AssertionError):
            read_all_file(filename=file_bad)

    @unittest.skip("does not yet wait for process to die")
    def test_gzip_file(self) -> None:
        read_all_file(filename=file_gzip)


ROWS = [["a", "b"], ["c", "d"]]


def write_rows(filename: str) -> None:
    with TsvWriter(filename=filename) as output_handle:
        for row in ROWS:
            output_handle.write(row)


class TestWriter(unittest.TestCase):

    def test_plain_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "out.tsv")
            write_rows(filename)
            with TsvReader(filename=filename) as input_handle:
                assert list(input_handle) == ROWS

    def test_gzip_by_file_name(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            filename = os.path.join(folder, "out.tsv.gz")
            write_rows(filename)
            with gzip.open(filename, mode="rt") as stream:
                assert stream.read() == "a\tb\nc\td\n"
