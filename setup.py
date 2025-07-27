#!/usr/bin/env python3
"""Setup script for Quickstart Prompt Generator CLI tool."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quickstart-prompt-generator",
    version="1.0.0",
    author="SDK Documentation Team",
    description="A CLI tool for generating LLM prompt templates for SDK quickstart documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
        "Jinja2>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "quickstart-prompt-generator=src.cli:main",
        ],
    },
)
