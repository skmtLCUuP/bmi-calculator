#!/usr/bin/env python3
"""
BMI Calculator Setup Configuration
SuperClaude Framework - 仕様駆動開発
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="bmi-calculator-gui",
    version="1.0.0",
    author="BMI Calculator Team",
    author_email="developer@bmi-calculator.com",
    description="Modern BMI Calculator with GUI and CLI interfaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skmtLCUuP/bmi-calculator",
    project_urls={
        "Bug Reports": "https://github.com/skmtLCUuP/bmi-calculator/issues",
        "Source": "https://github.com/skmtLCUuP/bmi-calculator",
        "Documentation": "https://github.com/skmtLCUuP/bmi-calculator/blob/main/README.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Desktop Environment",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "bmi-calculator=main:main",
            "bmi-gui=main:main",
        ],
    },
    keywords="bmi, health, calculator, gui, tkinter, customtkinter, who, body-mass-index",
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    include_package_data=True,
    zip_safe=False,
)