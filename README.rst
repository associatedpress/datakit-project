.. image:: https://img.shields.io/pypi/v/datakit-project.svg
        :target: https://pypi.python.org/pypi/datakit-project


.. image:: https://img.shields.io/travis/associatedpress/datakit-project.svg
    :target: https://travis-ci.org/associatedpress/datakit-project
    :alt: Linux build status on Travis CI


.. image:: https://readthedocs.org/projects/datakit-project/badge/?version=latest
    :target: https://datakit-project.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


===============================
datakit-project plugin
===============================

A datakit plugin for generating project skeletons from Cookiecutter_ templates.

Installation
============

For a system-wide install, at the command line::

    $ sudo pip install datakit-project

Usage
=====

`datakit-project` relies on the Cookiecutter_ library to generate project
templates from local git repositories as well as repositories hosted on Github.

Creating your first project
~~~~~~~~~~~~~~~~~~~~~~~~~~~
There are a few ways to create a project from a template::

    # From a local project
    $ datakit project:create --template /local/path/to/cookiecutter-basic-project

    # From Github
    $ datakit project:create --template https://github.com/associatedpress/cookiecutter-basic-project.git

    # From Github, but using an alias (less typing! WOOT!)
    $ datakit project:create --template gh:associatedpress/cookiecutter-basic-project

When you create a project, you will be prompted on the command-line for a series
of information. Fill in the info or hit *return* to accept defaults, as appropriate.

The project will be generated in the same directory where the command was invoked.


.. _default-template:

Default template
~~~~~~~~~~~~~~~~

As a convenience, the template used on your first project will be set as a 
default for future projects::

    $ datakit project::create # Uses cookiecutter-basic-project

You can update the default template by using the ``--make-default`` flag::

    $ datakit project:create --make-default --template gh:associatedpress/cookiecutter-some-other-project

Or you can directy edit the ``default_template`` variable in the :ref:`plugin-configuration`:

  .. code::

    # Edit ~/.datakit/plugins/datakit-project/config.json
    {"default_template": "/path/to/.cookiecutters/cookiecutter-basic-project"}


Installing more templates
~~~~~~~~~~~~~~~~~~~~~~~~~

Datakit suports use of more than one template. You simply need to specify the new template::

    $ datakit project:create --template gh:associatedpress/cookiecutter-some-other-project

Once installed locally, you can save a few key strokes::

    # Here, we drop the Github alias and organization
    $ datakit project:create --template cookiecutter-some-other-project

Or save yourself even more typing and make it the default template::

    $ datakit project:create --make-default --template cookiecutter-some-other-project

See :ref:`default-template` for more details on updating the default template.


Default user configs
====================

Save yourself even more typing -- picking up on a theme here? -- by creating a
user configuration file with your email and full name.

These values will be used as defaults whenever you create a new project.

These configs should be stored in a `cookiecutter user configuration file`_ located
at ``~/.cookiecutterrc``.

Add and customize the below settings to the config file:

  .. code::

    default_context:
        full_name: <Firstname Lastname>
        email: <your email>

**This is a YAML-format file, so pay close attention to formatting!**
In particular, note the single space after the ``full_name`` and ``email``
settings.


Templates
=========

Datakit stores new templates in the standard Cookiecutter_ location: ``~/.cookiecutters``.


.. _plugin-configuration:

Plugin Configuration
====================

By default, `datakit-project` stores its configurations in ``~/.datakit/plugins/datakit-project/config.json``.

.. _Cookiecutter: https://cookiecutter.readthedocs.io/en/latest/
.. _cookiecutter user configuration file: https://cookiecutter.readthedocs.io/en/latest/advanced/user_config.html
