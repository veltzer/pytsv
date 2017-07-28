import click
import pandas as pd
import numpy as np


@click.command()
@click.option(
    '--sample-column',
    required=True,
    type=str,
    help="what columns to split by, comma separated",
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
def main(
        factor_column,
        sample_columns,
        size,
        input_file,
        output_file,
):
    # type: (int, str, int, str, str) -> None
    """
    This application will sample a set of a tsv file.
    """
    sample_columns = [int(x) for x in sample_columns.split(',')]
    df = pd.read_csv(input_file, index_col=False, header=None, sep="\t")
    df.sample(n=size, weights=np.log2(df[factor_column]) + 1)[sample_columns].to_csv(
        output_file,
        sep='\t',
        index=False,
        header=None,
    )


if __name__ == '__main__':
    main()
