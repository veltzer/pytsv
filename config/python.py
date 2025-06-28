""" python deps for this project """

scripts: dict[str, str] = {
    "pytsv": "pytsv.main:main",
}

config_requires: list[str] = [
    "pyclassifiers",
]
install_requires: list[str] = [
    "pytconf",
    "tqdm",
    "pyanyzip",
    "numpy",
    "pandas",
    "pylogconf",
    "attrs",
]
build_requires: list[str] = [
    "hatch",
    "pydmt",
    "pymakehelper",
    # types 
    "pandas-stubs",
    "types-tqdm",
]
test_requires: list[str] = [
    "pylint",
    "pytest",
    "pytest-cov",
    "mypy",
    "ruff",
]
requires = config_requires + install_requires + build_requires + test_requires
