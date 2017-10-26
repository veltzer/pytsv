import click
import tqdm

from pytsv.pytsv import TsvReader, TsvWriter
import numpy.random


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
    elements = []
    with TsvReader(input_file) as input_handle:
        if progress:
            input_handle = tqdm.tqdm(input_handle)
        for fields in input_handle:
            elements.append(fields)
            weight = float(fields[sample_column])
            weights.append(weight)
    # the following code will only work on python3.6 because the
    # random.choices API was only introduced then
    # from random import choices
    # results = choices(lines, weights, k=size)

    # this is the same code with numpy
    results = [numpy.random.choice(elements, p=weights) for _ in range(size)]
    with TsvWriter(output_file) as output_handle:
        for result in results:
            output_handle.write(result)


if __name__ == '__main__':
    main()
