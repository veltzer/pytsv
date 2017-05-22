import setuptools

import sys
if not sys.version_info[0] == 3:
    sys.exit("Sorry, only python version 3 is supported")

setuptools.setup(
    name='pytsv',
    version='0.0.57',
    description='pytsv is a module to help with all things TSV',
    long_description='pytsv is a module to help with all things TSV',
    url='https://veltzer.github.io/pytsv',
    # bugtrack_url='https://github.com/veltzer/pytsv/issues',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='python TSV format csv',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    python_requires=">=3",
    install_requires=[
        'click',  # for command line parsing
        'tqdm',  # for progress report
        'pyanyzip',  # for opening zipped files
    ],
    entry_points={
        'console_scripts': [
            'pytsv_check=pytsv.scripts.check:main',
            'pytsv_aggregate=pytsv.scripts.aggregate:main',
            'pytsv_csv_to_tsv=pytsv.scripts.csv_to_tsv:main',
            'pytsv_tsv_to_csv=pytsv.scripts.tsv_to_csv:main',
            'pytsv_cut=pytsv.scripts.cut:main',
            'pytsv_split_by_columns=pytsv.scripts.split_by_columns:main',
            'pytsv_fix_field=pytsv.scripts.fix_field:main',
        ],
    },
)
