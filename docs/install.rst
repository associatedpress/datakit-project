Installation
============

Pre-flight check
~~~~~~~~~~~~~~~~

In order to use `datakit-project`, you must have:

* Python >= 3.10
* git_
* uv_

.. _git: https://git-scm.com/
.. _uv: https://docs.astral.sh/uv/

Install the plugin
~~~~~~~~~~~~~~~~~~

Install this plugin alongside datakit-core_. The recommended way is with uv_,
which keeps the ``datakit`` command and its plugins in a single isolated
environment::

    $ uv tool install datakit-core --with datakit-project

See the datakit-core_ docs for other ways to install and combine plugins.


.. _datakit-core: https://datakit-core.readthedocs.io/en/latest/


.. _plugin-configuration:

Plugin Configuration
~~~~~~~~~~~~~~~~~~~~

By default, `datakit-project` stores its configuration in ``~/.datakit/plugins/datakit-project/config.json``.

The one setting is the :ref:`default-template`. The recommended way to manage it
is with the generic ``datakit config`` command family that ships with
datakit-core_::

    $ datakit config set datakit-project default_template gh:associatedpress/cookiecutter-r-project
    $ datakit config list datakit-project

``datakit config`` writes the config file for you, so there's no need to
hand-edit it.
