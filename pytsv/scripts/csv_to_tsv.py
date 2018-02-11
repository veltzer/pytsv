import csv

import click

import pyanyzip.core
import sys

from pytsv.pytsv import TsvWriter


@click.command()
@click.option(
    '--input-file',
    required=True,
    type=str,
    help="input file",
    show_default=True,
)
@click.option(
    '--output-file',
    required=True,
    type=str,
    help="output file",
    show_default=True,
)
@click.option(
    '--set-max',
    required=True,
    type=bool,
    help="do you want to unset the limit on csv fields (good for large fielded csv files)",
    show_default=True,
)
def main(
        input_file,
        output_file,
        set_max,
):
    # type: (str, str, bool) -> None
    """ This script converts a CSV to a TSV file """
    if set_max:
        csv.field_size_limit(sys.maxsize)
    with pyanyzip.core.open(input_file, "rt") as input_file_handle:
        csv_reader = csv.reader(input_file_handle)
        with TsvWriter(output_file) as output_file_handle:
            for row in csv_reader:
                output_file_handle.write(row)


if __name__ == '__main__':
    main()
