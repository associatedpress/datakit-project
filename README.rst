===============================
datakit-project plugin
===============================

A datakit plugin for generating project skeletons from Cookiecutter_ templates.

* Free software: ISC license

============
Installation
============

At the command line::

    $ pip install datakit-project

=====
Usage
=====

Install Cookiecutter_ project templates::

    # Install from local project
    $ datakit project:add_template /path/to/cookiecutter-basic-project

    # Install from Github
    $ datakit project:add_template associatedpress/cookiecutter-basic-project

Create a project using locally installed template::

    $ datakit project:create new-project

.. _Cookiecutter: https://cookiecutter.readthedocs.io/en/latest/
