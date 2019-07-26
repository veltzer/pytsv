import config.project

package_name = config.project.project_name


console_scripts = [
    'pytsv=pytsv.endpoints.main:main',
]

setup_requires = [
]

run_requires = [
    'pytconf',  # for command line parsing
    'tqdm',  # for progress report
    'pyanyzip',  # for opening zipped files
    'numpy',  # for the histogram feature
    'pandas',  # for sample_by_column_pandas
    'pylogconf',  # for logging configuration
    'attrs',  # for attr like objects
]

test_requires = [
]

dev_requires = [
    'pyclassifiers',  # for programmatic classifiers
    # remarked for now
    # 'pypitools',  # for uploading to pypi
    'pydmt',  # for building easier
    'pylint',  # for checking the code
    'pytest',  # for testing the project
]

install_requires = list(setup_requires)
install_requires.extend(run_requires)

python_requires = ">=2.7"

extras_require={
    ':python_version == "2.7"': ['futures'],  # for python2.7 backport of concurrent.futures
}
