""" python deps for this project """

import config.shared

install_requires: list[str] = [
    "pytconf",
    "tqdm",
    "pyanyzip",
    "numpy",
    "pandas",
    "pylogconf",
    "attrs",
]
build_requires: list[str] = config.shared.PBUILD
test_requires: list[str] = config.shared.PTEST
types_required: list[str] = [
    "pandas-stubs",
    "types-tqdm",
]
requires = install_requires + build_requires + test_requires + types_required

scripts: dict[str, str] = {
    "pytsv": "pytsv.main:main",
}
