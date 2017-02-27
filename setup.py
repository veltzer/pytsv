import setuptools

import sys
if not sys.version_info[0] == 3:
    sys.exit("Sorry, only python version 3 is supported")

setuptools.setup(
    name='pytsv',
    version='0.0.1',
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
)
