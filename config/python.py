""" python depedencies for this project """

scripts: dict[str, str] = {
    "pytsv": "pytsv.main:main",
}
dev_requires: list[str] = [
]
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
    "pymakehelper",
    "pydmt",
    "pandas-stubs",
    "types-tqdm",
    "ruff",
]
test_requires: list[str] = [
    "pylint",
    "pytest",
    "pytest-cov",
    "mypy",
]
requires = config_requires + install_requires + build_requires + test_requires
