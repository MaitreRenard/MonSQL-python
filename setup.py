#!/usr/bin/env python3
#coding: utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="monsql-python",
    version="0.0.1",
    author="Masterfox, 0xNinja, Apollo",
    author_email="tom.mounet@pm.me",
    description="French overlay for MySQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MaitreRenard/MonSQL-python",
    packages=setuptools.find_packages(),
    install_requires=[
          'mysql-connector-python',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
