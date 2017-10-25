import csv

import click

import pyanyzip

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
def main(
        input_file,
        output_file,
):
    # type: (str, str) -> None
    """ This script converts a CSV to a TSV file """
    with pyanyzip.open(input_file, "rt") as input_file_handle:
        csv_reader = csv.reader(input_file_handle)
        with TsvWriter(output_file) as output_file_handle:
            for row in csv_reader:
                output_file_handle.write(row)


if __name__ == '__main__':
    main()
