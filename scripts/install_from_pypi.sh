#!/bin/sh

PIP=pip
PIP=pip3
sudo -H ${PIP} install --quiet --upgrade pytimer
${PIP} show pytimer | grep -e "^Version"
