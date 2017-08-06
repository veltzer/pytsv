import os
import click
import pytsv.pytsv


@click.command()
@click.option(
    '--input-folder',
    required=True,
    type=str,
    help="folder of input files",
    show_default=True,
)
@click.option(
    '--output-file',
    required=True,
    type=str,
    help="output file to generate",
    show_default=True,
)
@click.option(
    '--match-columns',
    required=True,
    type=str,
    help="column to match by",
    show_default=True,
)
@click.option(
    '--aggregate-columns',
    required=True,
    type=str,
    help="column to aggregate (must be numeric)",
    show_default=True,
)
@click.option(
    '--do-unlink',
    required=False,
    type=bool,
    default=False,
    help="remove files after done?",
    show_default=True,
)
def main(
        input_folder,
        output_file,
        match_columns,
        aggregate_columns,
        do_unlink,
):
    # type: (str, str, str, str, bool) -> None
    """ aggregate a bunch of tsv files """
    match_columns = [int(x) for x in match_columns.split(",")]
    aggregate_columns = [int(x) for x in aggregate_columns.split(",")]
    pytsv.pytsv.aggregate(
        input_file_names=os.listdir(input_folder),
        match_columns=match_columns,
        aggregate_columns=aggregate_columns,
        output_file_name=output_file,
        unlink=do_unlink,
    )

if __name__ == '__main__':
    main()
