# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='plugin2',
    version='0.0.1',
    author='messense',
    author_email='messense@icloud.com',
    url='https://github.com/messense/extender',
    packages=[
        'plugin2'
    ],
    description='test plugin 2',
    install_requires=[
        'extender',
    ],
    include_package_data=True,
    entry_points={
        'extender.plugins': [
            'plugin2 = plugin2.plugin:TestPlugin2',
        ]
    },
)