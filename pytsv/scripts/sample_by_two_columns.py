import click
import os
import pandas
from tqdm import tqdm


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
    '--group-column',
    required=True,
    type=int,
    help="what column to to determine group by",
)
@click.option(
    '--weight-column',
    required=True,
    type=int,
    help="what column to determine weight by",
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
    required=True,
    type=bool,
    help="allow replacement",
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
        group_column,
        weight_column,
        value_column,
        size,
        replace,
        progress,
):
    # type: (str, str, int, int, int, int, bool, bool) -> None
    """
    This application will sample from a tsv file by a sample column
    The sample column must be convertible to a floating point number.
    """
    df = pandas.read_csv(
        input_file,
        sep='\t',
        header=None,
    )
    clusters = df[group_column].unique()
    if progress:
        clusters = tqdm(clusters)
    if os.path.isfile(output_file):
        os.unlink(output_file)
    for cluster in clusters:
        cluster_queries = df[df[group_column] == cluster]
        sample = cluster_queries.sample(
            n=size,
            replace=replace,
            weights=cluster_queries[weight_column],
        )
        res = sample[sample.columns[value_column]].value_counts()
        res.to_csv(
            output_file,
            sep='\t',
            index=False,
            mode='a',
            header=None,
        )


if __name__ == '__main__':
    main()
