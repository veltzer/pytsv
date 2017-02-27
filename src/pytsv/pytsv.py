"""
Some utilities to do with tsv files
"""
import os
from collections import defaultdict
from typing import Iterable, List, Tuple, Dict
import itertools
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
