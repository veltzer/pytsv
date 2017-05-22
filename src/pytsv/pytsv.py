import gzip
import os
from collections import defaultdict
from typing import Iterable, List, Tuple, Dict, IO
import itertools
import logging
import re

import pyanyzip

logger = logging.getLogger(__name__)


def clean(text: str, clean_edges: bool=True, sub_trailing: bool=True, remove_non_ascii: bool=True) -> str:
    if sub_trailing:
        # replace all manner of whitespace (consecutive or not)
        # with s single space
        text = re.sub(r"[\r\t\n\v ]+", " ", text)
    if remove_non_ascii:
        text = text.encode('ascii', errors='ignore').decode()
    if clean_edges:
        # remove space from the left and right
        text = text.strip()
    return text


def aggregate(
        input_file_names: Iterable[str],
        match_columns: List[int],
        aggregate_columns: List[int],
        output_file_name: str,
        unlink=True) -> None:
    """
    This function aggregates a bunch of input files by integers.
    :param input_file_names:
    :param match_columns:
    :param aggregate_columns:
    :param output_file_name:
    :param unlink:
    :return:
    """
    counts = dict()  # type: Dict[Tuple[str], List[int]]
    for input_file_name in input_file_names:
        logger.debug("working on file [%s]", input_file_name)
        with open(input_file_name, 'rt') as file_handle:
            for line in file_handle:
                line = line.rstrip()
                parts = line.split("\t")  # type: List[str]
                # noinspection PyTypeChecker
                match = tuple([parts[i] for i in match_columns])  # type: Tuple[str]
                if match not in counts:
                    counts[match] = [int(0)] * len(aggregate_columns)
                for i, aggregate_column in enumerate(aggregate_columns):
                    counts[match][i] += int(parts[aggregate_column])
    with open(output_file_name, 'wt') as output_file_handle:  # type: IO[str]
        for match, aggregates in counts.items():
            print("\t".join(itertools.chain(match, [str(x) for x in aggregates])), file=output_file_handle)

    if unlink:
        for input_file_name in input_file_names:
            os.unlink(input_file_name)


def write_data(data: List[List[str]], output_file_name: str) -> None:
    with open(output_file_name, "at") as output_file_handle:  # type: IO[str]
        for d in data:
            print("\t".join(d), file=output_file_handle)


def group_by(
        input_file_names: Iterable[str],
        group_by_columns: List[int],
        collect_columns: List[int],
        output_file_template: str,
        unlink=True) -> List[str]:
    all_data = defaultdict(list)  # type: Dict[str, List[List[str]]]
    limit = 10000
    for input_file_name in input_file_names:
        logger.debug("working on file [%s]", input_file_name)
        with open(input_file_name, 'rt') as file_handle:
            for line in file_handle:
                line = line.rstrip()
                parts = line.split("\t")  # type: List[str]
                # noinspection PyTypeChecker
                match = tuple([parts[i] for i in group_by_columns])  # type: Tuple[str]
                match = "_".join(match)
                data_to_append = [parts[i] for i in collect_columns]
                all_data[match].append(data_to_append)
                if len(all_data[match]) > limit:
                    write_data(all_data[match], output_file_template.format(match=match))
                    all_data[match] = list()
    # write the rest for the data
    for match, data in all_data.items():
        write_data(data, output_file_template.format(match=match))
    # remove the input files
    if unlink:
        for input_file_name in input_file_names:
            os.unlink(input_file_name)
    return [output_file_template.format(match=match) for match in all_data]


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


class TsvWriter:
    def __init__(self, filename: str, sanitize: bool=True, throw_exceptions: bool=False,
                 clean_edges: bool=True, sub_trailing=True, fields_to_clean: List[int]=None,
                 check_num_fields: bool=True, num_fields: int=None, convert_to_string: bool=True,
                 remove_non_ascii: bool=True, do_gzip: bool=False, filename_detect: bool=True):
        if filename_detect:
            found = False
            if filename.endswith(".tsv.gz"):
                self.io = gzip.open(filename, mode="wt")  # type: IO[str]
                found = True
            if filename.endswith(".tsv"):
                self.io = open(filename, mode="wt")  # type: IO[str]
                found = True
            assert found
        else:
            if do_gzip:
                self.io = gzip.open(filename, mode="wt")  # type: IO[str]
            else:
                self.io = open(filename, mode="wt")  # type: IO[str]
        self.sanitize = sanitize
        self.throw_exceptions = throw_exceptions
        self.clean_edges = clean_edges
        self.sub_trailing = sub_trailing
        self.fields_to_clean = fields_to_clean
        if self.fields_to_clean is None:
            self.fields_to_clean = []
        self.check_num_fields = check_num_fields
        self.num_fields = num_fields
        self.convert_to_string = convert_to_string
        self.remove_non_ascii = remove_non_ascii

    def _sanitize(self, l: List[str]) -> None:
        if self.sanitize:
            for field in self.fields_to_clean:
                l[field] = clean(
                    text=l[field],
                    clean_edges=self.clean_edges,
                    sub_trailing=self.sub_trailing,
                    remove_non_ascii=self.remove_non_ascii,
                )

    def _convert(self, l: List[str]) -> None:
        if self.convert_to_string:
            for i, t in enumerate(l):
                if type(t) in (int, float):
                    l[i] = str(t)

    def write(self, l: List[str]) -> None:
        self._sanitize(l)
        if self.check_num_fields:
            if self.num_fields is None:
                self.num_fields = len(l)
            else:
                assert len(l) == self.num_fields, "wrong number of fields in {}".format(l)
        self._convert(l)
        print("\t".join(l), file=self.io)

    def close(self) -> None:
        self.io.close()

    def __enter__(self):
        """ method needed to be a context manager """
        return self

    def __exit__(self, itype, value, traceback):
        """ method needed to be a context manager """
        self.close()


class TsvReader:
    def __init__(self, filename: str, mode: str="rt", validate_all_lines_same_number_of_fields: bool=True,
                 use_any_format: bool=True, num_fields: int=None, skip_comments: bool=True,
                 check_non_ascii: bool=True):
        if use_any_format:
            self.io = pyanyzip.open(name=filename, mode=mode)
        else:
            self.io = open(filename, mode=mode)
        self.validate_all_lines_same_number_of_fields = validate_all_lines_same_number_of_fields
        self.num_fields = num_fields
        self.line_number = -1
        self.skip_comments = skip_comments
        self.check_non_ascii = check_non_ascii

    def __next__(self):
        """ method needed to be an iterator """
        self.line_number += 1
        line = self.io.readline()
        if not line:
            raise StopIteration
        if self.skip_comments:
            while line.startswith("#"):
                line = self.io.readline()
                if not line:
                    raise StopIteration
        line = line.rstrip('\r\n')
        if self.check_non_ascii:
            assert is_ascii(line), "non ascii characters in line [{}]".format(self.line_number)
        fields = line.split('\t')
        if self.validate_all_lines_same_number_of_fields:
            if self.num_fields is None:
                self.num_fields = len(fields)
            else:
                assert len(fields) == self.num_fields, "wrong number of fields in line number {} {} {}".format(
                    self.line_number,
                    self.num_fields,
                    len(fields),
                )
        if self.check_non_ascii:
            assert is_ascii(line)
        return fields

    def __iter__(self):
        """ method needed to be an iterator """
        return self

    def __enter__(self):
        """ method needed to be a context manager """
        return self

    def __exit__(self, itype, value, traceback):
        """ method needed to be a context manager """
        self.close()

    def close(self) -> None:
        self.io.close()


def write_dict(filename: str=None, d: Dict[str, str]=None) -> None:
    with TsvWriter(filename=filename, num_fields=2, fields_to_clean=[0]) as output_handle:
        for k, v in d.items():
            output_handle.write([k, v])
