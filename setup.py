"""

datakit-project
---------------

A project-skeleton generator for use with the `datakit <https://pypi.python.org/pypi/datakit-core/>`_ framework.

* `Code <https://github.com/associatedpress/datakit-project>`_
* `Docs <http://datakit-project.readthedocs.io/en/latest/>`_

"""
from setuptools import setup, find_packages

PROJECT = 'datakit-project'
VERSION = '0.3.1'

setup(
    name=PROJECT,
    version=VERSION,
    description="A datakit plugin to generate new projects.",
    long_description=__doc__,
    author="Serdar Tumgoren",
    author_email='zstumgoren@gmail.com',
    license="ISCL",
    url='https://github.com/associatedpress/datakit-project',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='datakit',
    platforms=['Any'],
    install_requires=[
        'click',
        'cliff',
        'cookiecutter>=1.6.0',
        'datakit-core',
        'prettytable'
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'datakit.plugins': [
            'project create = datakit_project:Create',
            'project templates = datakit_project:Templates',
            'project templates update = datakit_project:TemplatesUpdate',
        ]
    },
    test_suite='tests',
    tests_require=[
        'pytest',
        'pytest-catchlog',
    ],
    zip_safe=False,
)
