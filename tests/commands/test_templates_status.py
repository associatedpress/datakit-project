import os
import re
import shutil
import subprocess
from unittest import mock

import cookiecutter.config as cc_config
import pytest

from datakit_project import cookiecutters, Templates
from datakit_project import exceptions as dkit_exceptions


def test_noupdate_status(caplog, cookiecutter_home, deploy_template, monkeypatch, tmpdir):
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
              'Subject': 'Testing',
              'upstream_sha': 'a11706f',
              'upstream_date': '2017-02-02',
              'upstream_subject': 'Testing',
              'commits_behind': 'Up-to-date'
            },
            {
              'Name': 'fake-repo-two',
              'SHA': '55f62a0',
              'Date': '2019-03-06',
              'Subject': 'Testing',
              'upstream_sha': '55f62a0',
              'upstream_date': '2019-03-06',
              'upstream_subject': 'Testing',
              'commits_behind': 'Up-to-date'
            },
        ]
        # Run the command
        parsed_args = mock.Mock()
        # Set status flag to true
        parsed_args.status = True
        cmd = Templates(None, None, cmd_name='project templates')
        cmd.run(parsed_args)
        header = "Name            SHA       Date         Upstream SHA   Upstream Date   Commits behind"
        repo1 = "fake-repo       a11706f   2017-02-02   a11706f        2017-02-02      Up-to-date"
        repo2 = "fake-repo-two   55f62a0   2019-03-06   55f62a0        2019-03-06      Up-to-date"
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


def test_repo_behind_upstream(caplog, cookiecutter_home, deploy_template, monkeypatch, tmpdir):
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
              'Subject': 'Testing',
              'upstream_sha': 'c18705e',
              'upstream_date': '2017-06-01',
              'upstream_subject': 'Some newer commit',
              'commits_behind': 3
            },
            {
              'Name': 'fake-repo-two',
              'SHA': '55f62a0',
              'Date': '2019-03-06',
              'Subject': 'Testing',
              'upstream_sha': '55f62a0',
              'upstream_date': '2019-03-06',
              'upstream_subject': 'Testing',
              'commits_behind': 'Up-to-date'
            },
        ]
        # Run the command
        parsed_args = mock.Mock()
        # Set status flag to true
        parsed_args.status = True
        cmd = Templates(None, None, cmd_name='project templates')
        cmd.run(parsed_args)
        header = "Name            SHA       Date         Upstream SHA   Upstream Date   Commits behind"
        repo1 = "fake-repo       a11706f   2017-02-02   c18705e        2017-06-01      3"
        repo2 = "fake-repo-two   55f62a0   2019-03-06   55f62a0        2019-03-06      Up-to-date"
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
