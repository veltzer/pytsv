from __future__ import print_function

import gzip
import os
from collections import defaultdict
from typing import Iterable, List, Tuple, Dict, IO, Iterator
import itertools
import logging
import re

import pyanyzip


CHECK_NON_ASCII = False
SKIP_COMMENTS = True
VALIDATE_ALL_LINES_SAME_NUMBER_OF_FIELDS = True
USE_ANY_FORMAT = True
SANITIZE = True
CLEAN_EDGES = True
SUB_TRAILING = True
REMOVE_NON_ASCII = True
LOWER_CASE = True
CHECK_NUM_FIELDS = True
CONVERT_TO_STRING = True
DO_GZIP = False
FILENAME_DETECT = True


def clean(
        text,
        clean_edges=True,
        sub_trailing=True,
        remove_non_ascii=True,
        lower_case=True,
):
    # type: (str, bool, bool, bool, bool) -> str
    if sub_trailing:
        # replace all manner of whitespace (consecutive or not)
        # with s single space
        text = re.sub(r"[\r\t\n\v ]+", " ", text)
    if remove_non_ascii:
        text = text.encode('ascii', errors='ignore').decode()
    if clean_edges:
        # remove space from the left and right
        text = text.strip()
    if lower_case:
        text = text.lower()
    return text


def aggregate(
        input_file_names,
        match_columns,
        aggregate_columns,
        output_file_name,
        unlink=True,
):
    # type: (Iterable[str], List[int], List[int], str, bool) -> None
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
    logger = logging.getLogger(__name__)
    for input_file_name in input_file_names:
        logger.debug("working on file [%s]", input_file_name)
        with TsvReader(filename=input_file_name) as input_handle:
            for parts in input_handle:
                # noinspection PyTypeChecker
                match = tuple([parts[i] for i in match_columns])  # type: Tuple[str]
                if match not in counts:
                    counts[match] = [int(0)] * len(aggregate_columns)
                for i, aggregate_column in enumerate(aggregate_columns):
                    counts[match][i] += int(parts[aggregate_column])
    # notice that we create a writer that does not check the number
    # of fields because the check requires a len(fields) to be available
    # and it is not in this case because of itertools.chain
    with TsvWriter(
        filename=output_file_name,
        check_num_fields=False,
        sanitize=False,
    ) as output_file_handle:
        for match, aggregates in counts.items():
            to_write = itertools.chain(match, aggregates)  # type: List[str]
            output_file_handle.write(to_write)
    if unlink:
        for input_file_name in input_file_names:
            os.unlink(input_file_name)


def write_data(data, output_file_name):
    # type: (List[List[str]], str) -> None
    with TsvWriter(
            filename=output_file_name,
            mode="at",
    ) as output_file_handle:
        for d in data:
            output_file_handle.write(d)


def group_by(
        input_file_names,
        group_by_columns,
        collect_columns,
        output_file_template,
        unlink=True,
):
    # type: (Iterable[str], List[int], List[int], str, bool) -> List[str]
    all_data = defaultdict(list)  # type: Dict[str, List[List[str]]]
    limit = 10000
    logger = logging.getLogger(__name__)
    for input_file_name in input_file_names:
        logger.debug("working on file [%s]", input_file_name)
        with open(input_file_name, 'rt') as file_handle:
            for line in file_handle:
                line = line.rstrip()
                parts = line.split("\t")  # type: List[str]
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
    # type: (str) -> bool
    return all(ord(c) < 128 for c in s)


class TsvWriter(object):
    def __init__(
            self,
            filename,
            mode="wt",
            throw_exceptions=False,

            sanitize=SANITIZE,
            fields_to_clean=None,
            clean_edges=CLEAN_EDGES,
            sub_trailing=SUB_TRAILING,
            remove_non_ascii=REMOVE_NON_ASCII,
            lower_case=LOWER_CASE,

            check_num_fields=CHECK_NUM_FIELDS,
            num_fields=None,
            convert_to_string=CONVERT_TO_STRING,

            do_gzip=DO_GZIP,
            filename_detect=FILENAME_DETECT,
    ):
        # type: (str, str, bool, bool, List[int], bool, bool, bool, bool, bool, int, bool, bool, bool) -> None
        if filename_detect:
            found = False
            if filename.endswith(".tsv.gz"):
                self.io = gzip.open(filename, mode=mode)  # type: IO[str]
                found = True
            if filename.endswith(".tsv"):
                self.io = open(filename, mode=mode)  # type: IO[str]
                found = True
            assert found, "file name unknown"
        else:
            if do_gzip:
                self.io = gzip.open(filename, mode=mode)  # type: IO[str]
            else:
                self.io = open(filename, mode=mode)  # type: IO[str]
        self.throw_exceptions = throw_exceptions

        self.sanitize = sanitize
        self.fields_to_clean = fields_to_clean
        if self.fields_to_clean is None:
            self.fields_to_clean = []
        self.clean_edges = clean_edges
        self.sub_trailing = sub_trailing
        self.remove_non_ascii = remove_non_ascii
        self.lower_case = lower_case

        self.check_num_fields = check_num_fields
        self.num_fields = num_fields
        self.convert_to_string = convert_to_string

    def _sanitize(self, l):
        # type: (List[str]) -> None
        if self.sanitize:
            for field in self.fields_to_clean:
                l[field] = clean(
                    text=l[field],
                    clean_edges=self.clean_edges,
                    sub_trailing=self.sub_trailing,
                    remove_non_ascii=self.remove_non_ascii,
                    lower_case=self.lower_case,
                )

    def _convert(self, l):
        # type: (List[str]) -> Iterator[str]
        if self.convert_to_string:
            for i, t in enumerate(l):
                if type(t) in (int, float, type(None)):
                    yield str(t)
                else:
                    yield t
        else:
            for x in l:
                yield x

    def write(self, l):
        # type: (List[str]) -> None
        self._sanitize(l)
        if self.check_num_fields:
            if self.num_fields is None:
                self.num_fields = len(l)
            else:
                assert len(l) == self.num_fields, "wrong number of fields in {}".format(l)
        print("\t".join(self._convert(l)), file=self.io)

    def close(self):
        # type: () -> None
        self.io.close()

    def __enter__(self):
        """ method needed to be a context manager """
        return self

    def __exit__(self, itype, value, traceback):
        """ method needed to be a context manager """
        self.close()


class TsvReader:
    def __init__(
            self,
            filename,
            mode="rt",
            use_any_format=USE_ANY_FORMAT,
            validate_all_lines_same_number_of_fields=VALIDATE_ALL_LINES_SAME_NUMBER_OF_FIELDS,
            num_fields=None,
            skip_comments=SKIP_COMMENTS,
            check_non_ascii=CHECK_NON_ASCII,
    ):
        # type: (str, str, bool, bool, int, bool, bool) -> None
        if use_any_format:
            self.io = pyanyzip.open(name=filename, mode=mode)
        else:
            self.io = open(filename, mode=mode)
        self.validate_all_lines_same_number_of_fields = validate_all_lines_same_number_of_fields
        self.num_fields = num_fields
        self.skip_comments = skip_comments
        self.check_non_ascii = check_non_ascii

        self.line_number = -1

    def next(self):
        self.__next__()

    def __next__(self):
        """ method needed to be an iterator """
        self.line_number += 1
        # python2
        line = self.io.next()
        # python3
        # line = self.io.readline()
        if not line:
            raise StopIteration
        if self.skip_comments:
            while line.startswith("#"):
                # python2
                line = self.io.next()
                # python3
                # line = self.io.readline()
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

    def close(self):
        # type: () -> None
        self.io.close()


def write_dict(filename=None, d=None):
    # type: (str, Dict[str,str]) -> None
    with TsvWriter(filename=filename, num_fields=2, fields_to_clean=[0]) as output_handle:
        for k, v in d.items():
            output_handle.write([k, v])
