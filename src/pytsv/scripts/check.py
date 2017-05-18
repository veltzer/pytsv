import concurrent.futures
import os

import click
import tqdm

from pytsv.pytsv import TsvReader

"""
TODO:
- add ability to say how many lines are bad and print their content
"""


class ParamsForJob:
    def __init__(self):
        self.input_file = None
        self.num_fields = None
        self.validate_all_lines_same_number_of_fields = None
        self.check_non_ascii = None
        self.progress = None


def check_file(params_for_job: ParamsForJob) -> bool:
    print('checking [{}]...'.format(params_for_job.input_file))
    with TsvReader(filename=params_for_job.input_file, num_fields=params_for_job.num_fields,
                   validate_all_lines_same_number_of_fields=params_for_job.validate_all_lines_same_number_of_fields,
                   check_non_ascii=params_for_job.check_non_ascii) as input_file_handle:
        if params_for_job.progress:
            input_file_handle = tqdm.tqdm(input_file_handle)
        for _ in input_file_handle:
            pass
    return True


@click.command()
@click.option('--num-fields', required=False, default=None, type=int, help="how many fields should the tsv have")
@click.option('--progress', required=False, default=True, type=bool, help="show progress")
@click.option('--parallel', required=False, default=False, type=bool, help="check different files in parallel")
@click.option("--jobs", default=os.cpu_count(), help="how many jobs to run")
@click.option('--filename', required=False, default=True, type=bool, help="show filename")
@click.option('--check-non-ascii', required=False, default=True, type=bool, help="check non ascii")
@click.option('--validate_all_lines_same_number_of_fields', required=False, default=True, type=bool,
              help="validate all lines same number of fields")
@click.argument('input-files', nargs=-1)
def main(
        num_fields,
        progress,
        parallel,
        jobs,
        filename,
        check_non_ascii,
        validate_all_lines_same_number_of_fields,
        input_files,
):
    """ This script checks that every file given to it is legal tsv """
    if parallel:
        with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as executor:
            job_list = []
            for input_file in input_files:
                job = ParamsForJob()
                job.progress = progress
                job.check_non_ascii = check_non_ascii
                job.num_fields = num_fields
                job.input_file = input_file
                job.validate_all_lines_same_number_of_fields = validate_all_lines_same_number_of_fields
                job_list.append(job)
            results = list(executor.map(check_file, job_list))
        print(results)
    for input_file in input_files:
        if filename:
            print('checking [{}]...'.format(input_file))
        with TsvReader(filename=input_file, num_fields=num_fields,
                       validate_all_lines_same_number_of_fields=validate_all_lines_same_number_of_fields,
                       check_non_ascii=check_non_ascii) as input_file_handle:
            if progress:
                input_file_handle = tqdm.tqdm(input_file_handle)
            for _ in input_file_handle:
                pass


if __name__ == '__main__':
    main()
