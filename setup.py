# -*- coding: utf-8 -*-
from setuptools import setup

import extender
long_description = open('README.md').read()

setup(
    name='extender',
    version=extender.__version__,
    author='messense',
    author_email='messense@icloud.com',
    url='https://github.com/messense/extender',
    packages=[
        'extender'
    ],
    description='extender: A simple plug-in/extension system on Python',
    keywords='extender, plugin, extension',
    long_description=long_description,
    install_requires=[
        'six',
    ],
    include_package_data=True,
    license='MIT License',
    tests_require=['nose'],
    test_suite='nose.collector',
)