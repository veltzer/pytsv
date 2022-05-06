import config.project

package_name = config.project.project_name


console_scripts = [
    "pytsv=pytsv.main:main",
]

run_requires = [
    "pytconf",
    "tqdm",
    "pyanyzip",
    "numpy",
    "pandas",
    "pylogconf",
    "attrs",
]

test_requires = [
    "pylint",
    "pytest",
    "pytest-cov",
    "pyflakes",
    "flake8",
    "pymakehelper",
]

dev_requires = [
    "pyclassifiers",
    "pypitools",
    "pydmt",
]

python_requires = ">=3.9"
test_os = ["ubuntu-20.04"]
test_python = ["3.9"]
