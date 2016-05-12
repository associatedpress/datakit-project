#!/usr/bin/env python
# -*- coding: utf-8 -*-
PROJECT = 'datakit-plugins-project'
VERSION = '0.1'

import os
from setuptools import setup, find_packages



def dkit_home():
    user_home = os.path.expanduser('~')
    return os.path.join(user_home, '.datakit')

setup(
    name=PROJECT,
    version=VERSION,

    description="A datakit plugin to manage project CRUD",
    long_description="A longer readme with history of changes....",

    author="Serdar Tumgoren",
    author_email='zstumgoren@gmail.com',

    license="MIT",

    url='https://github.com/zstumgoren/datakit-plugins-project',

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

    install_requires=['cement', 'datakit'],

    packages=find_packages('src/datakit'),
    package_dir={'': 'src'},
    include_package_data=True,
    data_files=[
        (dkit_home() + '/plugins',   ['cli/project.py']),
        (dkit_home() + '/plugins.d', ['config/project.conf']),
    ],

    test_suite='tests',
    tests_require=['nose', 'mock'],
    zip_safe=False,
)
