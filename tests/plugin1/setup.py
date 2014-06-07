# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='plugin1',
    version='0.0.1',
    author='messense',
    author_email='messense@icloud.com',
    url='https://github.com/messense/extender',
    packages=[
        'plugin1'
    ],
    description='test plugin 1',
    install_requires=[
        'extender',
    ],
    include_package_data=True,
    entry_points={
        'extender.plugins': [
            'plugin1 = plugin1.plugin:TestPlugin1',
        ]
    },
)