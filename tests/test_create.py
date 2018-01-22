import os
import re
import shutil
import subprocess
from unittest import mock

import cookiecutter.config as cc_config
import pytest

from datakit_project import Create

from .helpers import (
    cookiecutter_home,
    create_plugin_config,
    datakit_home
)


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch, tmpdir):
    tmp_dir = tmpdir.strpath
    monkeypatch.setitem(
        cc_config.DEFAULT_CONFIG,
        'cookiecutters_dir',
        os.path.join(tmp_dir, '.cookiecutters')
    )
    monkeypatch.setenv('DATAKIT_HOME', datakit_home(tmp_dir))


def test_missing_config_file(caplog, tmpdir):
    """
    Create should auto-generate config file if it's missing
    """
    cmd = Create(None, None, cmd_name='project create')
    parsed_args = mock.Mock()
    parsed_args.template = ''
    parsed_args.make_default = False
    cmd.run(parsed_args)
    msg = 'No project templates have been installed'
    assert msg in caplog.text
    assert cmd.configs == {'default_template': ''}
    assert os.path.exists(cmd.plugin_config_path)


def test_warning_when_no_default_repo_setting(caplog, tmpdir):
    """
    Test CLI warning when 'project create' invoked for the first time
    without specifying a template
    """
    create_plugin_config(tmpdir.strpath)
    cmd = Create(None, None, cmd_name='project create')
    parsed_args = mock.Mock()
    parsed_args.template = ''
    parsed_args.make_default = False
    cmd.run(parsed_args)
    msg = 'No project templates have been installed'
    assert msg in caplog.text


def test_create_initial_project(caplog, monkeypatch, tmpdir):
    """
    Test creation of first project with specification of a
    local Cookiecutter template
    """
    create_plugin_config(tmpdir.strpath)
    fake_repo_path = os.path.join(os.getcwd(), 'tests/fake-repo')
    # Switch directories
    monkeypatch.chdir(tmpdir)
    # Run the command
    parsed_args = mock.Mock()
    parsed_args.template = fake_repo_path
    parsed_args.make_default = False
    cmd = Create(None, None, cmd_name='project create')
    cmd.run(parsed_args)
    # Tests:
    #  Project was created
    assert 'fake-project' in [pth.basename for pth in tmpdir.listdir()]
    #  Template set as default since it's first template encountered
    assert cmd.configs['default_template'] == fake_repo_path
    msg_pattern = r"Set default template to.+?fake-repo in plugin config (.+?config.json)"
    log_pattern_matches = True if re.search(msg_pattern, caplog.text) else False
    assert log_pattern_matches


def test_usage_of_default_template(monkeypatch, tmpdir):
    """
    Create should use the default template if a new template is not specified.
    """
    # Set up the configs to point default template at our fake repo
    fake_repo_path = os.path.join(os.getcwd(), 'tests/fake-repo')
    create_plugin_config(tmpdir.strpath, {'default_template': fake_repo_path})
    monkeypatch.chdir(tmpdir)
    parsed_args = mock.Mock()
    # NOTE: We're NOT specifying a template here, but we set the default above
    parsed_args.template = ''
    parsed_args.make_default = False
    cmd = Create(None, None, cmd_name='project create')
    cmd.run(parsed_args)
    assert 'fake-project' in [pth.basename for pth in tmpdir.listdir()]


def test_usage_of_nondefault_template(monkeypatch, tmpdir):
    """
    Create should support use of non-default template
    without overriding default template setting.
    """
    original_repo = os.path.join(os.getcwd(), 'tests/fake-repo')
    new_repo = os.path.join(os.getcwd(), 'tests/fake-repo-two')
    create_plugin_config(tmpdir.strpath, {'default_template': original_repo})
    monkeypatch.chdir(tmpdir)
    parsed_args = mock.Mock()
    parsed_args.template = new_repo
    parsed_args.make_default = False
    cmd = Create(None, None, cmd_name='project create')
    cmd.run(parsed_args)
    dir_contents = [pth.basename for pth in tmpdir.listdir()]
    assert 'fake-project' not in dir_contents
    assert 'fake-project-two' in dir_contents
    assert cmd.configs['default_template'] == original_repo


def test_new_default_template(caplog, monkeypatch, tmpdir):
    """
    Create should support ability to set a new default template.
    """
    original_repo = os.path.join(os.getcwd(), 'tests/fake-repo')
    new_repo = os.path.join(os.getcwd(), 'tests/fake-repo-two')
    create_plugin_config(tmpdir.strpath, {'default_template': original_repo})
    monkeypatch.chdir(tmpdir)
    # On first pass, we specify new template and set it as new default
    parsed_args = mock.Mock()
    parsed_args.template = new_repo
    parsed_args.make_default = True
    cmd = Create(None, None, cmd_name='project create')
    cmd.run(parsed_args)
    dir_contents = [pth.basename for pth in tmpdir.listdir()]
    assert 'fake-project' not in dir_contents
    assert 'fake-project-two' in dir_contents
    assert cmd.configs['default_template'].endswith('fake-repo-two')
    msg_pattern = r"Set default template to.+?fake-repo-two in plugin config (.+?config.json)"
    log_pattern_matches = True if re.search(msg_pattern, caplog.text) else False
    assert log_pattern_matches
    # Remove fake project and recreate without specifying the template
    # to ensure it's now applied as the default
    project_directory = os.path.join(tmpdir.strpath, 'fake-project-two')
    shutil.rmtree(project_directory)
    args_new = mock.Mock()
    args_new.template = ''
    cmd = Create(None, None, cmd_name='project create')
    cmd.run(args_new)
    dir_contents_updated = [pth.basename for pth in tmpdir.listdir()]
    assert 'fake-project' not in dir_contents_updated
    assert 'fake-project-two' in dir_contents_updated


def test_github_install(caplog, monkeypatch, tmpdir):
    # Copy
    cc_home = cookiecutter_home(tmpdir.strpath)
    orig_repo = os.path.join(os.getcwd(), 'tests/fake-repo')
    new_repo = os.path.join(cc_home, 'fake-repo')

    # Monkeypatch subprocess to prevent actual git clone
    # and simply copy over the repo instead
    def mockreturn(repo_bits, cwd, stderr):
        shutil.copytree(orig_repo, new_repo)
        return 'gh:associatedpress/fake-repo'

    monkeypatch.setattr(subprocess, 'check_output', mockreturn)
    monkeypatch.chdir(tmpdir)
    parsed_args = mock.Mock()
    # NOTE: We're NOT specifying a template here, but we set the default above
    parsed_args.template = 'gh:associatedpress/fake-repo'
    parsed_args.make_default = False
    cmd = Create(None, None, cmd_name='project create')
    cmd.run(parsed_args)
    assert 'fake-repo' in os.listdir(cc_home)
    assert cmd.configs['default_template'] == new_repo
