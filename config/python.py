import config.project

package_name = config.project.project_name


console_scripts = [
    'pytsv_aggregate=pytsv.scripts.aggregate:main',
    'pytsv_check=pytsv.scripts.check:main',
    'pytsv_check_columns_unique=pytsv.scripts.check_columns_unique:main',
    'pytsv_clean_by_field_num=pytsv.scripts.clean_by_field_num:main',
    'pytsv_csv_to_tsv=pytsv.scripts.csv_to_tsv:main',
    'pytsv_cut=pytsv.scripts.cut:main',
    'pytsv_drop_duplicates_by_columns=pytsv.scripts.drop_duplicates_by_columns:main',
    'pytsv_fix_columns=pytsv.scripts.fix_columns:main',
    'pytsv_histogram_by_column=pytsv.scripts.histogram_by_column:main',
    'pytsv_join=pytsv.scripts.join:main',
    'pytsv_lc=pytsv.scripts.lc:main',
    'pytsv_majority=pytsv.scripts.majority:main',
    'pytsv_multiply=pytsv.scripts.multiply:main',
    'pytsv_read=pytsv.scripts.read:main',
    'pytsv_remove_quotes=pytsv.scripts.remove_quotes:main',
    'pytsv_sample_by_column=pytsv.scripts.sample_by_column:main',
    'pytsv_sample_by_column_old=pytsv.scripts.sample_by_column_old:main',
    'pytsv_sample_by_two_columns=pytsv.scripts.sample_by_two_columns:main',
    'pytsv_split_by_columns=pytsv.scripts.split_by_columns:main',
    'pytsv_sum=pytsv.scripts.sum:main',
    'pytsv_tree=pytsv.scripts.tree:main',
    'pytsv_tsv_to_csv=pytsv.scripts.tsv_to_csv:main',
]

setup_requires = [
]

run_requires = [
    'click',  # for command line parsing
    'tqdm',  # for progress report
    'pyanyzip',  # for opening zipped files
    'numpy',  # for the histogram feature
    'futures',  # for python2.7 backport of concurrent.futures
    'pandas',  # for sample_by_column_pandas
    'pylogconf',  # for logging configuration
    'attrs',  # for attr like objects
]

test_requires = [
]

dev_requires = [
    'pyclassifiers',  # for programmatic classifiers
    # 'pypitools',  # for uploading to pypi
    # 'pydmt',  # for building easier
    'pylint',  # for checking the code
    'pytest',  # for testing the project
]

install_requires = list(setup_requires)
install_requires.extend(run_requires)

python_requires = ">=2.7"
