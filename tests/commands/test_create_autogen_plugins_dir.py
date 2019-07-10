import os
import re
import shutil
import subprocess
from unittest import mock

import pytest

from datakit_project import Create


# override the fixture defined in conftest.py
@pytest.fixture(autouse="module")
def create_plugin_dir():
    pass


def test_missing_config_file(caplog, tmpdir):
    """
    Create should auto-generate config file if it's missing
    """
    cmd = Create(None, None, cmd_name='project create')
    parsed_args = mock.Mock()
    parsed_args.template = ''
    parsed_args.make_default = False
    parsed_args.interactive = False
    cmd.run(parsed_args)
    msg = 'No project templates have been installed'
    assert msg in caplog.text
    assert cmd.configs == {'default_template': ''}
    assert os.path.exists(cmd.plugin_config_path)

