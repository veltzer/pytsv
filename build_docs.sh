#!/bin/sh -e
PACKAGE=pytsv
# either remove the files that sphinx-apidoc generated
# or pass a -f flag to it
#rm -f sphinx/$PACKAGE.rst sphinx/$PACKAGE.scripts.rst sphinx/modules.rst
sphinx-apidoc -f -o sphinx $PACKAGE > /dev/null


\rm -rf docs
# there is no need to pass '-b html' to sphinx-build since
# this is it's default
sphinx-build sphinx docs
