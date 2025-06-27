import setuptools


def get_readme():
    with open("README.rst") as f:
        return f.read()


setuptools.setup(
    name="pytsv",
    version="0.1.70",
    packages=[
    ],
    package_data={
		"pytsv": ["*.json"],
    },
    description="Pytsv is a the Swiss army knife for TSV files",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="Mark Veltzer",
    author_email="mark.veltzer@gmail.com",
    maintainer="Mark Veltzer",
    maintainer_email="mark.veltzer@gmail.com",
    keywords=[
        "python",
        "tsv",
        "format",
        "csv",
    ],
    url="https://veltzer.github.io/pytsv",
    download_url="https://github.com/veltzer/pytsv",
    license="MIT",
    platforms=[
        "python3",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
    ],
    install_requires=[
        "pytconf",
        "tqdm",
        "pyanyzip",
        "numpy",
        "pandas",
        "pylogconf",
        "attrs",
    ],
)
