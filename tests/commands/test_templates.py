import os
import re
import shutil
from unittest import mock

import cookiecutter.config as cc_config
import pytest

from datakit_project import Templates


@pytest.fixture
def deploy_template():
    copied_repos = []
    def _deploy_template(cc_home, repo_path):
        src_repo = repo_path
        base_name = repo_path.split('/')[-1]
        dest_repo = os.path.join(cc_home, base_name)
        shutil.copytree(src_repo, dest_repo)
        copied_repos.append(dest_repo)
        return dest_repo

    yield _deploy_template

    for repo in copied_repos:
        shutil.rmtree(repo)

def test_no_templates(caplog, cookiecutter_home, monkeypatch, tmpdir):
    """
    Templates should provide helpful info if no cookiecutter templates are installed
    """
    # Switch directories
    monkeypatch.chdir(tmpdir)
    # Run the command
    parsed_args = mock.Mock()
    cmd = Templates(None, None, cmd_name='project templates')
    cmd.run(parsed_args)
    assert cookiecutter_home in caplog.text
    assert "No project templates have been installed!" in caplog.text


def test_multiple_templates(caplog, cookiecutter_home, deploy_template, monkeypatch, tmpdir):
    """
    Templates should list installed cookiecutters
    """
    deploy_template(cookiecutter_home, 'tests/fake-repo')
    deploy_template(cookiecutter_home, 'tests/fake-repo-two')
    # Switch directories
    monkeypatch.chdir(tmpdir)
    # Run the command
    parsed_args = mock.Mock()
    cmd = Templates(None, None, cmd_name='project templates')
    cmd.run(parsed_args)
    msg_pattern = r"- fake-repo\n\t- fake-repo-two\n\nTo use a locally installed"
    log_pattern_matches = True if re.search(msg_pattern, caplog.text) else False
    assert log_pattern_matches

