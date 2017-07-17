import click
import tqdm

from pytsv.pytsv import TsvReader, TsvWriter


@click.command()
@click.option(
    '--progress',
    required=False,
    default=True,
    type=bool,
    help="show progress",
)
@click.option(
    '--cut-fields',
    required=True,
    type=str,
    help="fields to cut",
)
@click.option(
    '--input-file',
    required=True,
    type=str,
    help="input file (can be compressed)",
)
@click.option(
    '--output-file',
    required=True,
    type=str,
    help="output file (can be compressed)",
)
def main(
        progress: bool,
        cut_fields: str,
        input_file: str,
        output_file: str,
) -> None:
    """ cut fields from a tsv file """
    cut_fields = [int(x) for x in cut_fields.split(',') if x != ""]
    with TsvReader(filename=input_file) as input_file_handle:
        with TsvWriter(filename=output_file) as output_file_handle:
            if progress:
                input_file_handle = tqdm.tqdm(input_file_handle)
            for fields in input_file_handle:
                out_fields = [fields[x] for x in cut_fields]
                output_file_handle.write(out_fields)


if __name__ == '__main__':
    main()
