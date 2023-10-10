extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
]

import config.project
project = config.project.name
import config.personal
author = config.personal.fullname
from pydmt.helpers.signature import get_copyright_years_long
project_copyright = get_copyright_years_long(repo="..")+" "+author
import config.version
version = ".".join(str(x) for x in config.version.tup)
release = ".".join(str(x) for x in config.version.tup)

html_theme_options = {
        "show_powered_by": False,
}
rst_epilog = f"""
.. |project| replace:: {project}
"""
