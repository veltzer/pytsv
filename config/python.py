from typing import List


console_scripts: List[str] = [
    "pytsv=pytsv.main:main",
]
dev_requires: List[str] = [
    "pypitools",
]
config_requires: List[str] = [
    "pyclassifiers",
]
install_requires: List[str] = [
    "pytconf",
    "tqdm",
    "pyanyzip",
    "numpy",
    "pandas",
    "pylogconf",
    "attrs",
]
make_requires: List[str] = [
    "pymakehelper",
    "pydmt",
    "pandas-stubs",
    "types-tqdm",
]
test_requires: List[str] = [
    "pylint",
    "pytest",
    "pytest-cov",
    "pyflakes",
    "flake8",
    "mypy",
]
requires = config_requires + install_requires + make_requires + test_requires
