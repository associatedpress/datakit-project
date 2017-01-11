#!/usr/bin/env python
# -*- coding: utf-8 -*-
PROJECT = 'datakit-project'
VERSION = '0.1'

import os
from setuptools import setup, find_packages

setup(
    name=PROJECT,
    version=VERSION,

    description="A datakit plugin to manage project CRUD",
    long_description="A longer readme with history of changes....",

    author="Serdar Tumgoren",
    author_email='zstumgoren@gmail.com',

    license="MIT",

    url='https://github.com/zstumgoren/datakit-project',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console',
    ],

    keywords='datakit',
    platforms=['Any'],
    install_requires=['cliff', 'cookiecutter>=1.5.0'],
    packages=find_packages(),
    include_package_data=True,
    entry_points = {
        'datakit.plugins': [
            'project:create= datakit_project:Create',
        ]
    },
    test_suite='tests',
    tests_require=['pytest'],
    zip_safe=False,
)
