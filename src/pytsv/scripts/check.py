import click
import tqdm

from pytsv.pytsv import TsvReader

"""
TODO:
- add ability to say how many lines are bad and print their content
"""


@click.command()
@click.option('--num-fields', required=False, default=None, type=int, help="how many fields should the tsv have")
@click.option('--progress', required=False, default=True, type=bool, help="show progress")
@click.option('--filename', required=False, default=True, type=bool, help="show filename")
@click.option('--check-non-ascii', required=False, default=True, type=bool, help="check non ascii")
@click.option('--validate_all_lines_same_number_of_fields', required=False, default=True, type=bool,
              help="validate all lines same number of fields")
@click.argument('input-files', nargs=-1)
def main(num_fields, progress, filename, check_non_ascii, validate_all_lines_same_number_of_fields, input_files):
    """ This script checks that every file given to it is legal tsv """
    for input_file in input_files:
        if filename:
            print('checking [{}]...'.format(input_file))
        with TsvReader(filename=input_file, num_fields=num_fields,
                       validate_all_lines_same_number_of_fields=validate_all_lines_same_number_of_fields,
                       check_non_ascii=check_non_ascii) as input_file_handle:
            if progress:
                input_file_handle = tqdm.tqdm(input_file_handle)
            for _ in input_file_handle:
                pass


if __name__ == '__main__':
    main()
