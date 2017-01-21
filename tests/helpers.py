import os

from datakit.utils import mkdir_p

from datakit_project.utils import write_json


def cookiecutter_home(tmpdir):
    return os.path.join(tmpdir, '.cookiecutters')


def datakit_home(tmpdir):
    return os.path.join(tmpdir, '.datakit')


def create_cookiecutter_home(tmpdir):
    pth = cookiecutter_home(tmpdir)
    mkdir_p(pth)
    return pth


def create_plugin_config(root_dir, content={}):
    dkit_home = datakit_home(root_dir)
    plugin_dir = os.path.join(dkit_home, 'plugins/datakit-project')
    mkdir_p(plugin_dir)
    config_file = os.path.join(plugin_dir, 'config.json')
    config = {'default_template': ''}
    config.update(content)
    write_json(config_file, config)
    return config
