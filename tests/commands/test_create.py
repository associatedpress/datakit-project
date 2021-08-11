import os
import re
import shutil
import subprocess
from unittest import mock

import pytest

from datakit_project import Create


@pytest.mark.usefixtures('create_plugin_config_default')
def test_warning_when_no_default_repo_setting(caplog):
    """
    Test CLI warning when 'project create' invoked for the first time
    without specifying a template
    """
    cmd = Create(None, None, cmd_name='project create')
    parsed_args = mock.Mock()
    parsed_args.template = ''
    parsed_args.make_default = False
    parsed_args.interactive = False
    cmd.run(parsed_args)
    msg = 'No project templates have been installed'
    assert msg in caplog.text


@pytest.mark.usefixtures('create_plugin_config_default')
def test_create_initial_project(caplog, monkeypatch, tmpdir):
    """
    Test creation of first project with specification of a
    local Cookiecutter template
    """
    fake_repo_path = os.path.join(os.getcwd(), 'tests/fake-repo')
    # Switch directories
    monkeypatch.chdir(tmpdir)
    # Run the command
    parsed_args = mock.Mock()
    parsed_args.template = fake_repo_path
    parsed_args.make_default = False
    parsed_args.interactive = False
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


@pytest.mark.usefixtures('create_plugin_config_fake_repo')
def test_usage_of_default_template(monkeypatch, tmpdir):
    """
    Create should use the default template if a new template is not specified.
    """
    # Set up the configs to point default template at our fake repo
    monkeypatch.chdir(tmpdir)
    parsed_args = mock.Mock()
    # NOTE: We're NOT specifying a template here to
    # test usage of default set in fixture
    parsed_args.template = ''
    parsed_args.make_default = False
    parsed_args.interactive = False
    cmd = Create(None, None, cmd_name='project create')
    cmd.run(parsed_args)
    assert 'fake-project' in [pth.basename for pth in tmpdir.listdir()]


@pytest.mark.usefixtures('create_plugin_config_fake_repo')
def test_graceful_handling_of_project_overwrite_attempt(monkeypatch, tmpdir, caplog):
    """
    Create should exit gracefully and provide an appropriate
    error message when user provides a slug with the same name
    as an existing folder in the current working directory.
    """
    # Set up the configs to point default template at our fake repo
    monkeypatch.chdir(tmpdir)
    parsed_args = mock.Mock()
    parsed_args.template = ''
    parsed_args.make_default = False
    parsed_args.interactive = False
    parsed_args.overwrite_if_exists = False
    cmd = Create(None, None, cmd_name='project create')
    cmd.run(parsed_args)
    cmd.run(parsed_args)
    assert 'Error: A project with the slug you provided already exists in this directory. Try again with a different slug.' in caplog.text


@pytest.mark.usefixtures('create_plugin_config_fake_repo')
def test_usage_of_nondefault_template(monkeypatch, tmpdir):
    """
    Create should support use of non-default template
    without overriding default template setting.
    """
    original_repo = os.path.join(os.getcwd(), 'tests/fake-repo')
    new_repo = os.path.join(os.getcwd(), 'tests/fake-repo-two')
    monkeypatch.chdir(tmpdir)
    parsed_args = mock.Mock()
    parsed_args.template = new_repo
    parsed_args.make_default = False
    parsed_args.interactive = False
    cmd = Create(None, None, cmd_name='project create')
    cmd.run(parsed_args)
    dir_contents = [pth.basename for pth in tmpdir.listdir()]
    assert 'fake-project' not in dir_contents
    assert 'fake-project-two' in dir_contents
    assert cmd.configs['default_template'] == original_repo


@pytest.mark.usefixtures('create_plugin_config_fake_repo')
def test_new_default_template(caplog, monkeypatch, tmpdir):
    """
    Create should support ability to set a new default template.
    """
    original_repo = os.path.join(os.getcwd(), 'tests/fake-repo')
    new_repo = os.path.join(os.getcwd(), 'tests/fake-repo-two')
    monkeypatch.chdir(tmpdir)
    # On first pass, we specify new template and set it as new default
    parsed_args = mock.Mock()
    parsed_args.template = new_repo
    parsed_args.make_default = True
    parsed_args.interactive = False
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
    args_new.interactive = False
    cmd = Create(None, None, cmd_name='project create')
    cmd.run(args_new)
    dir_contents_updated = [pth.basename for pth in tmpdir.listdir()]
    assert 'fake-project' not in dir_contents_updated
    assert 'fake-project-two' in dir_contents_updated


def test_github_install(caplog, monkeypatch, cookiecutter_home, tmpdir):
    orig_repo = os.path.join(os.getcwd(), 'tests/fake-repo')
    new_repo = os.path.join(cookiecutter_home, 'fake-repo')

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
    parsed_args.interactive = False
    cmd = Create(None, None, cmd_name='project create')
    cmd.run(parsed_args)
    assert 'fake-repo' in os.listdir(cookiecutter_home)
    assert cmd.configs['default_template'] == new_repo
