#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='mypackage',
    version='0.0.1',
    author='First Last',
    author_email='first.last@example.com',
    url='https://github.com/firstlast/mypackage',
    description='Dummy package demonstrating ways of collecting coverage',
    long_description='Dummy package demonstrating ways of collecting coverage',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages(where='src', exclude=('tests',)),
    #packages=find_packages(exclude=('tests',)),
    zip_safe=True,
)
