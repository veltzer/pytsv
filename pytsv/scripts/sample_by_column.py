from random import choices

import click
import tqdm

from pytsv.pytsv import TsvReader, TsvWriter


@click.command()
@click.option(
    '--input-file',
    required=True,
    type=str,
    help="input filename",
    show_default=True,
)
@click.option(
    '--output-file',
    required=True,
    type=str,
    help="output filename",
    show_default=True,
)
@click.option(
    '--sample-column',
    required=True,
    type=int,
    help="what column to sample by",
    show_default=True,
)
@click.option(
    '--size',
    required=True,
    type=int,
    help="what sample size do you need?",
    show_default=True,
)
@click.option(
    '--progress',
    required=False,
    default=True,
    type=bool,
    help="show progress",
    show_default=True,
)
def main(
        input_file,
        output_file,
        sample_column,
        size,
        progress,
):
    # type: (str, str, int, int, bool) -> None
    """
    This application will sample from a tsv file by a sample column
    The sample column must be convertible to a floating point number.
    """
    weights = []
    lines = []
    with TsvReader(input_file) as input_handle:
        if progress:
            input_handle = tqdm.tqdm(input_handle)
        for fields in input_handle:
            lines.append(fields)
            weight = float(fields[sample_column])
            weights.append(weight)
    results = choices(lines, weights, k=size)
    with TsvWriter(output_file) as output_handle:
        for result in results:
            output_handle.write(result)


if __name__ == '__main__':
    main()
