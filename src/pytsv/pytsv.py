import os
from collections import defaultdict
from typing import Iterable, List, Tuple, Dict
import itertools
import logging
import re

import pyanyzip

logger = logging.getLogger(__name__)


def clean(text: str, clean_edges: bool=True, sub_trailing: bool=True) -> str:
    if sub_trailing:
        # make sure we have just one space between words
        # make sure that text does not contain tabs
        text = re.sub(r"[\r\t\n\v ]+", " ", text)
    if clean_edges:
        # remove space from the left and right
        text = text.strip()
    # TODO: get rid of strings which are binary or not well encoded
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
    with open(output_file_name, 'wt') as output_file_handle:
        for match, aggregates in counts.items():
            print("\t".join(itertools.chain(match, [str(x) for x in aggregates])), file=output_file_handle)

    if unlink:
        for input_file_name in input_file_names:
            os.unlink(input_file_name)


def write_data(data: List[List[str]], output_file_name: str) -> None:
    with open(output_file_name, "at") as output_file_handle:
        for d in data:
            print("\t".join(d), file=output_file_handle)


def group_by(
        input_file_names: Iterable[str],
        group_by_columns: List[int],
        collect_columns: List[int],
        output_file_template: str,
        unlink=True) -> List[str]:
    all_data = defaultdict(list)  # type: Dict[str, List[List[str]]]
    LIMIT = 10000
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
                if len(all_data[match]) > LIMIT:
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


class TsvWriter:
    def __init__(self, filename: str, sanitize: bool=True, throw_exceptions: bool=False,
                 clean_edges: bool=True, sub_trailing=True, fields_to_clean: List[int]=None,
                 check_num_fields: bool=True, num_fields: int=None, convert_to_string: bool=True):
        self.io = open(filename, mode="wt")
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

    def _sanitize(self, l: List[str]) -> None:
        if self.sanitize:
            for field in self.fields_to_clean:
                l[field] = clean(text=l[field], clean_edges=self.clean_edges, sub_trailing=self.sub_trailing)

    def _convert(self, l: List[str]) -> None:
        if self.convert_to_string:
            for i, t in enumerate(l):
                if type(t) in (int, float):
                    l[i] = str(t)

    def write(self, l: List[str]) -> None:
        self._sanitize(l)
        if self.check_num_fields:
            assert len(l) == self.num_fields, "wrong number of fields in {}".format(l)
        self._convert(l)
        print("\t".join(l), file=self.io)

    def close(self) -> None:
        self.io.close()

    @staticmethod
    def open(filename: str, sanitize: bool=True, throw_exceptions: bool=False,
             clean_edges: bool=True, sub_trailing: bool=True, fields_to_clean=None,
             check_num_fields: bool=True, num_fields: int=None, convert_to_string: bool=True):
        return TsvWriter(filename=filename, sanitize=sanitize, throw_exceptions=throw_exceptions,
                         clean_edges=clean_edges, sub_trailing=sub_trailing,
                         fields_to_clean=fields_to_clean, check_num_fields=check_num_fields,
                         num_fields=num_fields, convert_to_string=convert_to_string)


class TsvReader:
    def __init__(self, filename: str, mode: str="rt", validate_all_lines_same_number_of_fields: bool=True,
                 use_any_format: bool=True, num_fields: int=None):
        if use_any_format:
            self.io = pyanyzip.open(name=filename, mode=mode)
        else:
            self.io = open(filename, mode=mode)
        self.validate_all_lines_same_number_of_fields = validate_all_lines_same_number_of_fields
        self.num_fields = num_fields

    def __next__(self):
        """ method needed to be an iterator """
        line = self.io.readline()
        if not line:
            raise StopIteration
        line = line.rstrip('\r\n')
        fields = line.split('\t')
        if self.validate_all_lines_same_number_of_fields:
            if self.num_fields is None:
                self.num_fields = len(fields)
            else:
                assert len(fields) == self.num_fields
        return fields

    def __iter__(self):
        """ method needed to be an iterator """
        return self

    def __enter__(self):
        """ method needed to be a context manager """
        pass

    def __exit__(self, itype, value, traceback):
        """ method needed to be a context manager """
        self.close()

    def close(self) -> None:
        print("in close")
        self.io.close()
