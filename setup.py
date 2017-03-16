import setuptools

import sys
if not sys.version_info[0] == 3:
    sys.exit("Sorry, only python version 3 is supported")

setuptools.setup(
    name='pytsv',
    version='0.0.21',
    description='pytsv is a module to help with all things TSV',
    long_description='pytsv is a module to help with all things TSV',
    url='https://veltzer.github.io/pytsv',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='python TSV format csv',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    install_requires=[
        'click',  # for command line parsing
        'tqdm',  # for progress report
    ],
    entry_points={
        'console_scripts': [
            'pytsv_check=pytsv.check:main',
            'pytsv_aggregate=pytsv.aggregate:main',
            'pytsv_csv_to_tsv=pytsv.csv_to_tsv:main',
            'pytsv_cut=pytsv.cut:main'
        ],
    },
)
