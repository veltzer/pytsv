import csv

import click

import pyanyzip


@click.command()
@click.option('--input-file', required=True, type=str, help="input file")
@click.option('--output-file', required=True, type=str, help="output file")
def main(input_file, output_file):
    """ This script converts a CSV to a TSV file """
    with pyanyzip.open(input_file, "rt") as input_file_handle:
        r = csv.reader(input_file_handle)
        with open(output_file) as output_file_handle:
            for row in r:
                output_file_handle.write(row)

if __name__ == '__main__':
    main()
