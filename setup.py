#!/usr/bin/env python

from glob import glob

import os
import codecs
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pyspresso',
    use_scm_version=True,
    description='A Raspberry Pi Espresso machine PID controller',
    author='Andreas Pelme',
    author_email='andreas@pelme.se',
    url='https://github.com/pelme/pyspresso',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    long_description=read('README.rst'),
    install_requires=[
        'click==5.1',
        'cffi==1.1.2',
        'RPi.GPIO==0.5.11',
        'smbus-cffi==0.4.1',
        'gpiozero==0.9.0',
    ],
    setup_requires=[
        'setuptools_scm==1.7.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': [
            'pyspressod=pyspresso.bin.pyspressod:main',
            'temp_debug=pyspresso.bin.temp_debug:main',
        ]
    },
)
