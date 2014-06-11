# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='plugin3',
    version='0.0.1',
    author='messense',
    author_email='messense@icloud.com',
    url='https://github.com/messense/extender',
    packages=[
        'plugin3'
    ],
    description='test plugin 3',
    install_requires=[
        'extender',
    ],
    include_package_data=True,
    entry_points={
        'extender.plugins': [
            'plugin3 = plugin3.plugin:TestPlugin3',
        ]
    },
)
