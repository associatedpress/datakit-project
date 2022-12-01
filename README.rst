.. image:: https://img.shields.io/pypi/v/datakit-project.svg
    :target: https://pypi.python.org/pypi/datakit-project

.. image:: https://img.shields.io/pypi/pyversions/datakit-project.svg
    :target: https://pypi.python.org/pypi/datakit-project

.. image:: https://img.shields.io/travis/associatedpress/datakit-project.svg
    :target: https://travis-ci.org/associatedpress/datakit-project
    :alt: Linux build status on Travis CI

.. image:: https://readthedocs.org/projects/datakit-project/badge/
    :target: http://datakit-project.readthedocs.io/en/latest/
    :alt: Documentation Status

Datakit
=======

Datakit is a pluggable command-line tool for managing the life cycle
of data projects.

The Associated Press Data Team uses Datakit to auto-generate project skeletons,
archive and share data on Amazon S3, and other routine tasks.

Datakit is a thin wrapper around the Cliff_ command-line framework and
is intended for use with a growing ecosystem of plugins.

Overview
========

`datakit-project` provides command-line tools to help generate project skeletons from Cookiecutter_ templates.
The plugin is part of the `datakit command-line framework`_.

Some highlights include the ability to:

* Install templates from local Git repos or from Github
* Interactively select a template when creating new projects
* List locally installed templates
* Check whether templates are out-of-date
* Update templates

The Associated Press Data Team relies on this plugin because it fits nicely into a
broader data science workflow built around datakit.

It's worth noting that Cookiecutter's command-line tool offers some of these features, and its developers
are working to add others. Additionally, we primarily support Git-based templates,
whereas Cookiecutter also works with mercurial repositories.

Please be sure to check out the latest release of Cookiecutter to see
if it might be a better fit.

.. _Cookiecutter: https://cookiecutter.readthedocs.io/en/latest/
.. _datakit command-line framework: https://datakit.ap.org/

https://datakit-core.readthedocs.io/en/latest/readme.html
