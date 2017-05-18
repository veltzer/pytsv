import os
import click
import pytsv.pytsv


@click.command()
@click.option('--folder', required=True, type=str, help="folder")
@click.option('--output-file', required=True, type=str, help="folder")
@click.option('--match-columns', required=True, type=str, help="column to match by")
@click.option('--aggregate-columns', required=True, type=str, help="column to aggregate (must be numeric)")
@click.option('--do-unlink', required=False, type=bool, default=True, help="remove files after done?")
def main(
        folder: str,
        output_file: str,
        match_columns: str,
        aggregate_columns: str,
        do_unlink: bool,
) -> None:
    """ aggregate a bunch of tsv files """
    match_columns = [int(x) for x in match_columns.split(",")]
    aggregate_columns = [int(x) for x in aggregate_columns.split(",")]
    pytsv.pytsv.aggregate(
        input_file_names=os.listdir(folder),
        match_columns=match_columns,
        aggregate_columns=aggregate_columns,
        output_file_name=output_file,
        unlink=do_unlink,
    )

if __name__ == '__main__':
    main()
