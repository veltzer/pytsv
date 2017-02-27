import os
import click
import pytsv


@click.command()
def main():
    """ aggregate a bunch of tsv files """
    pytsv.pytsv.aggregate(
        input_file_names=[x for x in os.listdir(".")],
        match_columns=[0, 1],  # columns to match by
        aggregate_columns=[2],  # columns to aggregate (must be numeric)
        output_file_name="final_output.tsv",
        unlink=True,
    )

if __name__ == '__main__':
    main()
