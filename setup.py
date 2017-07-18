#! /usr/bin/env python3
from setuptools import setup

setup(
    name="prniolet",
    version="0.0.1",
    author="Christoph Heuel",
    author_email="christoph@heuel-web.de",
    license="MIT",
    install_requires=['python-escpos', 'aiomas[mp]'],
    scripts=['scripts/prniolet-server', 'scripts/prniolet-xkcd'],
)
