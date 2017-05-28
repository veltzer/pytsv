from typing import List

import click
import tqdm
from pytsv import pytsv

from pytsv.pytsv import TsvReader, TsvWriter


@click.command()
@click.option('--progress', required=False, default=True, type=bool, help="show progress")
@click.option('--input-file', required=True, type=str, help="input file")
@click.option('--output-file', required=True, type=str, help="output file")
@click.option('--fix-columns', required=True, type=str, help="columns to fix")
@click.option('--clean-edges', required=False, default=True, type=bool, help="remove space before and after")
@click.option('--sub-trailing', required=False, default=True, type=bool,
              help="substitute consecutive white spaces with one single space")
@click.option('--remove-non-ascii', required=False, default=True, type=bool, help="remove non ascii characters")
@click.option('--lower-case', required=False, default=True, type=bool, help="lower case the field")
def main(
        progress: bool,
        input_file: str,
        output_file: str,
        fix_columns: str,
        clean_edges: bool,
        sub_trailing: bool,
        remove_non_ascii: bool,
        lower_case: bool,
) -> None:
    """
    This script will fix a tsv file assuming that bad characters or tabs have been
left in one column of it.
    """
    fix_columns = [int(x) for x in fix_columns.split(',')]
    with TsvReader(filename=input_file) as input_file_handle:
        if progress:
            input_file_handle = tqdm.tqdm(input_file_handle)
        with TsvWriter(filename=output_file) as output_file_handle:
            for fields in input_file_handle:  # type: List[str]
                for fix_column in fix_columns:
                    fields[fix_column] = pytsv.clean(
                        text=fields[fix_column],
                        clean_edges=clean_edges,
                        sub_trailing=sub_trailing,
                        remove_non_ascii=remove_non_ascii,
                        lower_case=lower_case,
                    )
                output_file_handle.write(fields)

if __name__ == '__main__':
    main()
