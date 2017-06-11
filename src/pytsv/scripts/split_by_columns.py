from typing import List

import click
import logging

import pylogconf
import tqdm

from pytsv.pytsv import TsvReader, TsvWriter


@click.command()
@click.option('--columns', required=True, type=str, help="what columns to split by, comma separated")
@click.option('--pattern', required=False, default="{key}.tsv.gz", type=str, help="pattern of generated files")
@click.option('--progress', required=False, default=True, type=bool, help="show progress")
@click.argument('input-files', nargs=-1)
def main(
        columns: str,
        pattern: str,
        progress: bool,
        input_files: List[str],
) -> None:
    """
    This application will split a TSV file into many files according
    to some of its columns
    """
    pylogconf.setup()
    logger = logging.getLogger(__name__)
    columns = [int(x) for x in columns.split(',') if x != ""]
    assert len(columns) > 0, "must provide --columns"
    tsv_writers_dict = dict()
    for input_file in input_files:
        with TsvReader(filename=input_file) as input_file_handle:
            if progress:
                logger.info("working on [%s]" % input_file)
                input_file_handle = tqdm.tqdm(input_file_handle)
            for fields in input_file_handle:
                key = ",".join([fields[x] for x in columns])
                if key not in tsv_writers_dict:
                    filename = pattern.format(key=key)
                    output_handle = TsvWriter(filename=filename)
                    tsv_writers_dict[key] = output_handle
                output_handle = tsv_writers_dict[key]
                output_handle.write(fields)
    # close all writers
    for v in tsv_writers_dict.values():
        v.close()

if __name__ == '__main__':
    main()
