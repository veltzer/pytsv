import click
import tqdm

from pytsv.pytsv import TsvReader, TsvWriter

"""
This application will split a TSV file into many files according
to some of its columns
"""


@click.command()
@click.option('--columns', required=True, type=str, help="what columns to split by, comma separated")
@click.option('--pattern', required=False, default="{key}.tsv", type=str, help="pattern of generated files")
@click.option('--progress', required=False, default=True, type=bool, help="show progress")
@click.option('--input-file', required=True, type=str, help="filename to work on")
def main(columns, pattern, progress, input_file):
    """ split a tsv file according to columns """
    columns = [int(x) for x in columns.split(',') if x != ""]
    assert len(columns) > 0, "must provide --columns"
    tsv_writers_dict = dict()
    with TsvReader(filename=input_file) as input_file_handle:
        if progress:
            input_file_handle = tqdm.tqdm(input_file_handle)
        for fields in input_file_handle:
            key = ",".join([fields[x] for x in columns])
            if key not in tsv_writers_dict:
                filename = pattern.format(key=key)
                output_handle = TsvWriter.open(filename=filename)
                tsv_writers_dict[key] = output_handle
            output_handle = tsv_writers_dict[key]
            output_handle.write(fields)
    # close all writes
    for v in tsv_writers_dict.values():
        v.close()

if __name__ == '__main__':
    main()
