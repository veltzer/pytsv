from typing import List

import click
import tqdm

from pytsv.pytsv import TsvReader, TsvWriter

"""
This script will fix a tsv file assuming that bad characters or tabs have been
left in one column of it.
"""


@click.command()
@click.option('--progress', required=False, default=True, type=bool, help="show progress")
@click.option('--input-file', required=True, type=str, help="input file")
@click.option('--output-file', required=True, type=str, help="output file")
@click.option('--num-columns', required=True, type=int, help="num columns")
@click.option('--fix-column', required=True, type=int, help="column to fix")
def main(progress, input_file, output_file, num_columns, fix_column):
    """ fix a field in a tsv file """
    count_fixed = 0
    with TsvReader(filename=input_file, validate_all_lines_same_number_of_fields=False)\
            as input_file_handle:
        if progress:
            input_file_handle = tqdm.tqdm(input_file_handle)
        with TsvWriter(filename=output_file) as output_file_handle:
            for fields in input_file_handle:  # type: List[str]
                if len(fields) != num_columns:
                    count_fixed += 1
                    fixed_field = " ".join(fields[fix_column:len(fields)-num_columns+fix_column+1])
                    new_fields = fields[:fix_column]
                    new_fields.append(fixed_field)
                    new_fields.extend(fields[fix_column:len(fields)-num_columns+fix_column:])
                    output_file_handle.write(new_fields)
                else:
                    output_file_handle.write(fields)


if __name__ == '__main__':
    main()
