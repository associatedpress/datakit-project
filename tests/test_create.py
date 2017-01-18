import os
import re
from unittest import mock

import cookiecutter.config as cc_config
import pytest

from datakit_project import Create

from .helpers import (
    create_plugin_config,
    datakit_home
)


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch, tmpdir):
    tmp_dir = tmpdir.strpath
    monkeypatch.setitem(
        cc_config.DEFAULT_CONFIG,
        'cookiecutters_dir',
        tmp_dir
    )
    monkeypatch.setenv('DATAKIT_HOME', datakit_home(tmp_dir))
    create_plugin_config(tmp_dir)


def test_warning_when_no_default_repo(caplog):
    """
    Test CLI warning when project:create invoked for the first time
    without specifying a template
    """
    cmd = Create(None, None, cmd_name='project:create')
    parsed_args = mock.Mock()
    parsed_args.template = ''
    cmd.run(parsed_args)
    msg = 'No project templates have been installed'
    assert msg in caplog.text


def test_create_initial_project(caplog, monkeypatch, tmpdir):
    """
    Test creation of first project with specification of a
    local Cookiecutter template
    """
    # NOTE: using a template with preset defaults to sidestep need for
    # passing no_input=True flag. For examples requiring input,
    # Cookiecutter prompts for input and tests fail with:
    #   OSError: reading from stdin while output is captured)
    fake_repo_path = os.path.join(os.getcwd(), 'tests/fake-repo')
    # Switch directories
    monkeypatch.chdir(tmpdir)
    # Run the command
    parsed_args = mock.Mock()
    parsed_args.template = fake_repo_path
    cmd = Create(None, None, cmd_name='project:create')
    cmd.run(parsed_args)
    # Tests:
    #  Project was created
    assert 'fake-project' in [pth.basename for pth in tmpdir.listdir()]
    #  Template set as default since it's first template encountered
    assert cmd.configs['default_template'] == fake_repo_path
    msg_pattern = r"Set default template to.+?fake-repo in plugin config (.+?config.json)"
    log_pattern_matches = True if re.search(msg_pattern, caplog.text) else False
    assert log_pattern_matches


# TODO: test default_template is used after initial project creation
# TODO: test default_template is NOT updated if it's a subsequent project install
# TODO: test defalt_template is updated if flag is passed
# TODO: test that non-default template is used when specified
# TODO: test default_template path that does not exist (e.g. of template was local and has since been moved)
