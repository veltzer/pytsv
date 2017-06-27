import concurrent.futures
import logging
import os
from typing import List, Dict

import attr
import click
import pylogconf
import tqdm

from pytsv.pytsv import TsvReader, TsvWriter


@attr.attrs
class JobInfo:
    check_not_ascii = attr.attrib()  # type: bool
    input_file = attr.attrib()  # type: str
    serial = attr.attrib()  # type: int
    progress = attr.attrib()  # type: bool
    pattern = attr.attrib()  # type: str
    columns = attr.attrib()  # type: List[int]


@attr.attrs
class JobReturnValue:
    serial = attr.attrib()  # type: int
    files = attr.attrib()  # type: Dict[str, str]


def process_single_file(job_info: JobInfo) -> JobReturnValue:
    logger = logging.getLogger(__name__)
    tsv_writers_dict = dict()
    results = dict()
    with TsvReader(
            filename=job_info.input_file,
            check_non_ascii=job_info.check_non_ascii
    ) as input_file_handle:
        if job_info.progress:
            logger.info("working on [%s]" % job_info.input_file)
            input_file_handle = tqdm.tqdm(input_file_handle)
        for fields in input_file_handle:
            key = ",".join([fields[x] for x in job_info.columns])
            if key not in tsv_writers_dict:
                filename = job_info.pattern.format(key=key, i=job_info.serial)
                results[key] = filename
                output_handle = TsvWriter(filename=filename)
                tsv_writers_dict[key] = output_handle
            output_handle = tsv_writers_dict[key]
            output_handle.write(fields)
    for v in tsv_writers_dict.values():
        v.close()
    return JobReturnValue(job_info.serial, results)


@click.command()
@click.option('--columns', required=True, type=str, help="what columns to split by, comma separated")
@click.option('--pattern', required=False, default="{key}_{i:04d}.tsv.gz", type=str, help="pattern of generated files")
@click.option('--final-pattern', required=False, default="{key}.tsv.gz", type=str, help="pattern of generated files")
@click.option('--progress', required=False, default=True, type=bool, help="show progress")
@click.option("--jobs", default=os.cpu_count(), help="how many jobs to run")
@click.option('--check_non_ascii', required=False, default=True, type=bool, help="check for non ascii characters")
@click.argument('input-files', nargs=-1)
def main(
        columns: str,
        pattern: str,
        final_pattern: str,
        progress: bool,
        jobs: int,
        check_non_ascii: bool,
        input_files: List[str],
) -> None:
    """
    This application will split a TSV file into many files according
    to some of its columns
    """
    pylogconf.setup()
    columns = [int(x) for x in columns.split(',') if x != ""]
    assert len(columns) > 0, "must provide --columns"
    job_data = [JobInfo(
        check_non_ascii,
        input_file,
        i,
        progress,
        pattern,
        columns,
    ) for i, input_file in enumerate(input_files)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as executor:
        job_return_values = list(executor.map(process_single_file, job_data))  # type: List[JobReturnValue]
    job_return_values.sort(key=lambda x: x.serial)
    for job_return_value in job_return_values:
        for key, filename in job_return_value.files.items():
            outfile = final_pattern.format(key=key)
            with open(outfile, "wb") as _:
                pass
                # with open(filename, "rb") as _:


if __name__ == '__main__':
    main()