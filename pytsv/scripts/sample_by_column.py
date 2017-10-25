import click
import pandas as pd
import numpy as np


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
    type=str,
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
def main(
        input_file,
        output_file,
        sample_column,
        size,
):
    # type: (str, str, int, int) -> None
    """
    This application will sample from a tsv file by a weight column
    """
    df = pd.read_csv(input_file, index_col=False, header=None, sep="\t")
    df.sample(n=size, weights=np.log2(df[sample_column]) + 1).to_csv(
        output_file,
        sep='\t',
        index=False,
        header=None,
    )


if __name__ == '__main__':
    main()
