import click

import pandas


@click.command()
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
@click.option(
    '--weight-column',
    required=True,
    type=int,
    help="what column to sample by",
)
@click.option(
    '--value-column',
    required=True,
    type=int,
    help="what is the value column",
)
@click.option(
    '--size',
    required=True,
    type=int,
    help="what sample size do you need?",
)
@click.option(
    '--replace',
    required=False,
    type=bool,
    default=False,
    help="allow replacements?",
)
def main(
        input_file,
        output_file,
        weight_column,
        value_column,
        size,
        replace,
):
    # type: (str, str, int, int, int, bool) -> None
    """
    This application will sample from a tsv file by a sample column
    The sample column must be convertible to a floating point number.
    """
    df = pandas.read_csv(
        input_file,
        sep='\t',
        header=None,
    )
    sample = df.sample(
        n=size,
        replace=replace,
        weights=df[weight_column],
    )
    res = sample[sample.columns[value_column]].value_counts()
    res.to_csv(
        output_file,
        sep='\t',
        index=True,
    )


if __name__ == '__main__':
    main()
