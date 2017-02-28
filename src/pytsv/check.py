import click
import sys


@click.command()
@click.option('--num-fields', required=True, type=int, help="how many fields should the tsv have")
@click.argument('input-files', nargs=-1)
def main(num_fields, input_files):
    """ This script checks that every file given to it is legal tsv """
    for input_file in input_files:
        with open(input_file, "rt") as input_file_handle:
            for line in input_file_handle:
                line = line.rstrip('\r\n')
                parts = line.split("\t")
                if len(parts) != num_fields:
                    print("line [{}] in file [{}] has errors has [{}] parts instead of [{}]".format(
                        line, input_file, len(parts), num_fields))
                    sys.exit(1)


if __name__ == '__main__':
    main()
