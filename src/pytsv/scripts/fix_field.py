from typing import List

import click
import tqdm
from pytsv import pytsv

from pytsv.pytsv import TsvReader, TsvWriter


@click.command()
@click.option('--progress', required=False, default=True, type=bool, help="show progress")
@click.option('--input-file', required=True, type=str, help="input file")
@click.option('--output-file', required=True, type=str, help="output file")
@click.option('--fix-column', required=True, type=int, help="column to fix")
@click.option('--clean-edges', required=False, type=bool, help="remove space before and after")
@click.option('--sub-trailing', required=False, type=bool,
              help="substitute consecutive white spaces with one single space")
@click.option('--remove-non-ascii', required=False, type=bool, help="remove non ascii characters")
def main(
        progress: bool,
        input_file: str,
        output_file: str,
        fix_column: int,
        clean_edges: bool,
        sub_trailing: bool,
        remove_non_ascii: bool,
) -> None:
    """
    This script will fix a tsv file assuming that bad characters or tabs have been
left in one column of it.
    """
    with TsvReader(filename=input_file) as input_file_handle:
        if progress:
            input_file_handle = tqdm.tqdm(input_file_handle)
        with TsvWriter(filename=output_file) as output_file_handle:
            for fields in input_file_handle:  # type: List[str]
                num_columns = len(fields)
                fixed_field = " ".join(fields[fix_column:len(fields)-num_columns+fix_column+1])
                fixed_field = pytsv.clean(
                    text=fixed_field,
                    clean_edges=clean_edges,
                    sub_trailing=sub_trailing,
                    remove_non_ascii=remove_non_ascii,
                )
                new_fields = fields[:fix_column]
                new_fields.append(fixed_field)
                new_fields.extend(fields[len(fields)-fix_column:])
                output_file_handle.write(new_fields)

if __name__ == '__main__':
    main()
