import click
import tqdm

from pytsv.pytsv import TsvReader


@click.command()
@click.option('--num-fields', required=False, default=None, type=int, help="how many fields should the tsv have")
@click.option('--progress', required=False, default=True, type=bool, help="show progress")
@click.argument('input-files', nargs=-1, help="the files to check")
def main(num_fields, progress, input_files):
    """ This script checks that every file given to it is legal tsv """
    for input_file in input_files:
        with TsvReader(filename=input_file, num_fields=num_fields) as input_file_handle:
            if progress:
                input_file_handle = tqdm.tqdm(input_file_handle)
            for _ in input_file_handle:
                pass


if __name__ == '__main__':
    main()
