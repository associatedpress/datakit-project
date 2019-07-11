Managing Templates
==================

Datakit stores new templates in the standard Cookiecutter_ location: ``~/.cookiecutters``.


Installing templates
~~~~~~~~~~~~~~~~~~~~

Datakit suports use of more than one template. You simply need to specify the new template
when creating a new project::

    $ datakit project create --template gh:associatedpress/cookiecutter-some-other-project

The above command will install the template locally, so it can be used in future projects.

See :ref:`saving-keystrokes` and :ref:`interactive-template-selection` for details on using locally 
installed templates.


.. _templates-command:

Listing templates
~~~~~~~~~~~~~~~~~

To view all templates installed locally, use the below command::

   $ datakit project templates


Template status
~~~~~~~~~~~~~~~

Templates installed from Github may get new features and bugfixes over time. To quickly check
if a locally installed template is out-of-date, use the following command::

   $ datakit project templates --status

Updating templates
~~~~~~~~~~~~~~~~~~

To fetch the latest changes for locally installed templates, use the following command::

   $ datakit project templates update


.. _default-template:

Default template
~~~~~~~~~~~~~~~~

As a convenience, the first template you install (see :ref:`create-your-first-project`) will be
set as the default for future projects. This allows you to skip specifying a
template on subsequent projects::

    $ datakit project create

You can update the default template by using the ``--make-default`` flag::

    $ datakit project create --make-default --template gh:associatedpress/cookiecutter-some-other-project

Or you can directy edit the ``default_template`` variable in the :ref:`plugin-configuration`:

  .. code::

    # Edit ~/.datakit/plugins/datakit-project/config.json
    {"default_template": "/path/to/.cookiecutters/cookiecutter-basic-project"}


.. _Cookiecutter: https://cookiecutter.readthedocs.io/en/latest/
.. _many Cookiecutters: https://cookiecutter.readthedocs.io/en/latest/readme.html#available-cookiecutters
