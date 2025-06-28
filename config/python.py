""" python deps for this project """

import config.shared

scripts: dict[str, str] = {
    "pytsv": "pytsv.main:main",
}

config_requires: list[str] = config.shared.PCONFIG
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
requires = config_requires + install_requires + build_requires + test_requires + types_required
