#! /usr/bin/env python3
from setuptools import setup

setup(
    name="prniotlet",
    version="0.2.1",
    author="Christoph Heuel",
    author_email="christoph@heuel-web.de",
    license="MIT",
    install_requires=['python-escpos', 'aiomas[mp]', 'click'],
    packages=setuptools.find_packages(),
    scripts=[
        'scripts/prniotlet-server', 'scripts/prniotlet-xkcd',
        'scripts/prniotlet-wlan', 'scripts/prniotlet-advent',
        'scripts/prniotlet-text',
    ],
)
