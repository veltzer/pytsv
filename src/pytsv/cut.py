import click
import tqdm

from pytsv.pytsv import TsvReader


@click.command()
@click.option('--num-fields', required=False, default=None, type=int, help="how many fields should the tsv have")
@click.option('--progress', required=False, default=True, type=bool, help="show progress")
@click.option('--cut-fields', required=True, default="", type=str, help="fields to cut")
@click.argument('input-files', nargs=-1)
def main(num_fields, progress, cut_fields, input_files):
    """ cut fields from tsv files """
    cut_fields = [int(x) for x in cut_fields.split(',')]
    for input_file in input_files:
        with TsvReader(filename=input_file, num_fields=num_fields, validate_all_lines_same_number_of_fields=True)\
                as input_file_handle:
            if progress:
                input_file_handle = tqdm.tqdm(input_file_handle)
            for fields in input_file_handle:
                out_fields = [fields[x] for x in cut_fields]
                print("\t".join(out_fields))


if __name__ == '__main__':
    main()
