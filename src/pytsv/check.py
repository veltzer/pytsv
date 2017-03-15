import click

from pytsv.pytsv import TsvWriter


@click.command()
@click.option('--num-fields', required=False, default=None, type=int, help="how many fields should the tsv have")
@click.argument('input-files', nargs=-1)
def main(num_fields, input_files):
    """ This script checks that every file given to it is legal tsv """
    for input_file in input_files:
        with TsvWriter.open(filename=input_file, num_fields=num_fields) as input_file_handle:
            for _ in input_file_handle:
                pass


if __name__ == '__main__':
    main()
