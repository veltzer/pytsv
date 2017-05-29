import csv
import click
from pytsv.pytsv import TsvReader


@click.command()
@click.option('--input-file', required=True, type=str, help="input file")
@click.option('--output-file', required=True, type=str, help="output file")
def main(
        input_file: str,
        output_file: str,
) -> None:
    """ This script converts a TSV file to a CSV file """
    with open(output_file, "wt") as output_file_handle:
        csv_writer = csv.writer(output_file_handle)
        with TsvReader(input_file) as input_file_handle:
            for fields in input_file_handle:
                csv_writer.writerow(fields)


if __name__ == '__main__':
    main()
