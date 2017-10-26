import click

import numpy.random


@click.command()
def main(
):
    # type: () -> None
    """
    Test application
    """
    print(numpy.version.full_version)


if __name__ == '__main__':
    main()
