# -*- coding: utf-8 -*-
from setuptools import setup

long_description = open('README.md').read()

setup(
    name='extender',
    version='0.0.6',
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
        'six>=1.6.1',
        'nose>=1.3.3',
    ],
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
)