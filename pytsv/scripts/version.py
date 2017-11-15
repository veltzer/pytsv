import click

import numpy.random

import pytsv.version


@click.command()
@click.option(
    '--version',
    required=False,
    default=False,
    type=bool,
    help="show version",
    show_default=True,
)
def main(
    version,
):
    # type: (bool) -> None
    """
    Test application
    """
    if version:
        print(pytsv.version.version_str)
        return
    print(numpy.version.full_version)


if __name__ == '__main__':
    main()
