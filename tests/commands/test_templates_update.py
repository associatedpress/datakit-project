import os
import re
import shutil
from unittest import mock

import cookiecutter.config as cc_config
import pytest

from datakit_project import cookiecutters, TemplatesUpdate


def test_nothing_to_update(caplog):
    with mock.patch('datakit_project.commands.templates_update.Cookiecutters') as MockClass:
        instance = MockClass.return_value
        instance.info.return_value = [{
          'Name': 'fake-repo', 'SHA': 'a11706f', 'Date': '2017-02-02',
          'Subject': 'Testing', 'upstream_sha': 'a11706f',
          'upstream_date': '2017-02-02', 'upstream_subject': 'Testing',
          'commits_behind': 'Up-to-date'
        }]
        instance.upstream_tracking_branch.return_value = 'origin/master'
        # Run the command
        parsed_args = mock.Mock()
        cmd = TemplatesUpdate(None, None, cmd_name='project templates update')
        cmd.run(parsed_args)
        instance.info.assert_called_once_with(status=True)
        assert "Local templates are all up-to-date" in caplog.text

@pytest.mark.parametrize("repo_info, selection, expected",
    [
        # Select "all" out-of-date repos
        (
            [{
              'Name': 'fake-repo', 'SHA': 'a11706f', 'Date': '2017-02-02',
              'Subject': 'Testing', 'upstream_sha': 'c18705e',
              'upstream_date': '2017-06-01', 'upstream_subject': 'Some newer commit',
              'commits_behind': 3
            },
            {
              'Name': 'fake-repo-two', 'SHA': '55f62a0', 'Date': '2019-03-06',
              'Subject': 'Testing', 'upstream_sha': '55f62a0',
              'upstream_date': '2019-03-06', 'upstream_subject': 'Testing',
              'commits_behind': 'Up-to-date'
            }],
            ['all'],
            ['fake-repo']
        ),
        # Select single option
        (
            [{
              'Name': 'fake-repo', 'SHA': 'a11706f', 'Date': '2017-02-02',
              'Subject': 'Testing', 'upstream_sha': 'c18705e',
              'upstream_date': '2017-02-02', 'upstream_subject': 'Some newer commit',
              'commits_behind': 3
            },
            {
              'Name': 'fake-repo-two', 'SHA': '55f62a0', 'Date': '2019-03-06',
              'Subject': 'Testing', 'upstream_sha': '55f62a0',
              'upstream_date': '2019-03-06', 'upstream_subject': 'Testing',
              'commits_behind': 'Up-to-date'
            }],
            ['1'],
            ['fake-repo']
        ),
        # Select subset of out-of-date repos
        (
            [{
              'Name': 'fake-repo', 'SHA': 'a11706f', 'Date': '2017-02-02',
              'Subject': 'Testing', 'upstream_sha': 'c18705e',
              'upstream_date': '2017-02-02', 'upstream_subject': 'Some newer commit',
              'commits_behind': 3
            },
            {
              'Name': 'fake-repo-two', 'SHA': '55f62a0', 'Date': '2019-03-06',
              'Subject': 'Testing', 'upstream_sha': '32a42b0',
              'upstream_date': '2019-03-07', 'upstream_subject': 'A newer commit',
              'commits_behind': 1
            }],
            ['1'],
            ['fake-repo']
        ),
        # Select multiple out-of-date repos
        (
            [{
              'Name': 'fake-repo', 'SHA': 'a11706f', 'Date': '2017-02-02',
              'Subject': 'Testing', 'upstream_sha': 'c18705e',
              'upstream_date': '2017-02-02', 'upstream_subject': 'Some newer commit',
              'commits_behind': 3
            },
            {
              'Name': 'fake-repo-two', 'SHA': '55f62a0', 'Date': '2019-03-06',
              'Subject': 'Testing', 'upstream_sha': '32a42b0',
              'upstream_date': '2019-03-07', 'upstream_subject': 'A newer commit',
              'commits_behind': 1
            }],
            ['1', '2'],
            ['fake-repo', 'fake-repo-two']
        ),
    ]
)
def test_update(repo_info, selection, expected, monkeypatch):
    with mock.patch('datakit_project.commands.templates_update.Cookiecutters') as MockClass:
        instance = MockClass.return_value
        instance.info.return_value = repo_info
        instance.upstream_tracking_branch.return_value = 'origin/master'
        monkeypatch.setattr(
            'datakit_project.commands.templates_update.read_multichoice_or_all_input',
            lambda choices: selection
        )
        # Run the command
        parsed_args = mock.Mock()
        cmd = TemplatesUpdate(None, None, cmd_name='project templates update')
        cmd.run(parsed_args)
        instance.info.assert_called_once_with(status=True)
        instance.update.assert_called_once_with(expected)
