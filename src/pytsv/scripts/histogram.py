import click
import numpy

from pytsv.pytsv import TsvReader, TsvWriter


@click.command()
@click.option('--input-file', required=True, type=str, help="input file")
@click.option('--output-file', required=True, type=str, help="output file")
@click.option('--column-number', required=True, type=int, help="what column to histogram")
@click.option('--bucket-number', required=False, default=10, type=int, help="what column to histogram")
def main(
        input_file: str,
        output_file: str,
        column_number: int,
        bucket_number: int,
) -> None:
    """ Create a histogram from a field in a tsv file """
    a = []
    with TsvReader(input_file) as input_handle:
        for fields in input_handle:
            a.append(fields[column_number])
    count_in_bucket, bucket_edges = numpy.histogram(a, bins=bucket_number)
    with TsvWriter(output_file) as output_handle:
        for i, count in enumerate(count_in_bucket):
            edge_from = bucket_edges[i]
            edge_to = bucket_edges[i+1]
            output_handle.write([
                edge_from,
                edge_to,
                count,
            ])

if __name__ == '__main__':
    main()
