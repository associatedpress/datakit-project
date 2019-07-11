Installation
============

Pre-flight check
~~~~~~~~~~~~~~~~

In order to use `datakit-project`, you must have:

* Python >= 3.5
* git_

.. _git: https://git-scm.com/

Install the plugin
~~~~~~~~~~~~~~~~~~

For a `user install`_ from the command line::

    $ pip install --user datakit-project


.. _user install: https://pip.pypa.io/en/stable/user_guide/#user-installs


.. _plugin-configuration:

Plugin Configuration
~~~~~~~~~~~~~~~~~~~~

By default, `datakit-project` stores its configurations in ``~/.datakit/plugins/datakit-project/config.json``.

For example, the plugin configuration file contains the setting for the :ref:`default-template`:

.. code::

   {"default_template": "/path/to/.cookiecutters/cookiecutter-basic-project"}
