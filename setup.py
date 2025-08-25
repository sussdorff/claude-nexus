#!/usr/bin/env python
"""Setup script for claude-nexus."""

from setuptools import setup, find_packages

setup(
    packages=find_packages(),
    package_data={
        "nexus": ["py.typed"],
    },
)