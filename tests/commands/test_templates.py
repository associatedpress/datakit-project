import os
import re
import shutil
from unittest import mock

import cookiecutter.config as cc_config
import pytest

from datakit_project import cookiecutters, Templates


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
    # Mock the return value for Cookiecutters.info
    with mock.patch('datakit_project.commands.templates.Cookiecutters') as MockClass:
        instance = MockClass.return_value
        instance.info.return_value = [
            {
              'Name': 'fake-repo',
              'SHA': 'a11706f',
              'Date': '2017-02-02',
              'Subject': 'Testing'
            },
            {
              'Name': 'fake-repo-two',
              'SHA': '55f62a0',
              'Date': '2019-03-06',
              'Subject': 'Testing'
            },
        ]
        # Run the command
        parsed_args = mock.Mock()
        parsed_args.status = False
        cmd = Templates(None, None, cmd_name='project templates')
        cmd.run(parsed_args)
        header = "Name            SHA       Date         Subject"
        repo1 = "fake-repo       a11706f   2017-02-02   Testing"
        repo2 = "fake-repo-two   55f62a0   2019-03-06   Testing"
        expected = [header, repo1, repo2]
        # Some gross cleanup of caplog.text is necessary because it displays log level info
        actual = [re.sub(r"templates.py\s+\d+\sINFO", "", line).strip()  for line in caplog.text.split('\n')]
        # Test that expected lines appear in displayed text
        for line in expected:
            assert line in actual
        # Test alpha sortting by repo name
        header_idx = actual.index(header)
        repo1_idx = actual.index(repo1)
        repo2_idx = actual.index(repo2)
        assert header_idx < repo1_idx
        assert repo1_idx < repo2_idx
