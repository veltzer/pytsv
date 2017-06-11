import click
import pandas as pd
import numpy as np


@click.command()
@click.option(
    '--sample-column',
    required=True,
    type=str,
    help="what columns to split by, comma separated",
)
@click.option(
    '--size',
    required=True,
    type=int,
    help="what sample size do you need?",
)
@click.option(
    '--input-file',
    required=True,
    type=str,
    help="input filename",
)
@click.option(
    '--output-file',
    required=True,
    type=str,
    help="output filename",
)
def main(
        factor_column: int,
        sample_columns: str,
        size: int,
        input_file: str,
        output_file: str,
) -> None:
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
