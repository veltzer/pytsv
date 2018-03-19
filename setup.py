import setuptools

import pytsv.version

setuptools.setup(
    name='pytsv',
    version=pytsv.version.version_str,
    description='pytsv is a module to help with all things TSV',
    long_description='pytsv is a module to help with all things TSV',
    url='https://veltzer.github.io/pytsv',
    download_url='https://github.com/veltzer/pytsv',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    license='MIT',
    platforms=['python'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='python TSV format csv',
    packages=setuptools.find_packages(),
    install_requires=[
        'click',  # for command line parsing
        'tqdm',  # for progress report
        'pyanyzip',  # for opening zipped files
        'numpy',  # for the histogram feature
        'futures',  # for python2.7 backport of concurrent.futures
        'pandas',  # for sample_by_column_pandas
    ],
    entry_points={
        # order here is by order of files in the scripts folder
        'console_scripts': [
        ],
    },
)
