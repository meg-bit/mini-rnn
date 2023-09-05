# This file is part of argseq
# Released under the MIT License (see LICENSE file)

import os
import sys
import subprocess
import shutil

try:
    import setuptools
except ImportError:
    sys.exit("setuptools Not Found. "
             "Install setuptools with 'pip install setuptools'.")

from setuptools import setup

# Make sure setup.py in run in the directory
script_dir = os.path.dirname(os.path.realpath(__file__))
if script_dir != os.getcwd():
    os.chdir(script_dir)

from argseq.__version__ import __version__

setup(
    name='argseq',
    version=__version__,
    description='De novo assembler for single molecule sequencing reads using repeat graphs',
    url='https://github.com/meg-bit/long-read-aligner',
    author='Meg Paiva',
    author_email = 'margaretpaiva20@gmail.com',
    license='MIT',
    packages=['argseq'],
    python_requires='>=3.10',
    install_requires=[
        'numpy',
        'scipy',
        'pysam',
        'pyabpoa',
        'medaka',
    ]
)
