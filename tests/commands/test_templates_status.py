import os
import re
import shutil
import subprocess
from unittest import mock

import cookiecutter.config as cc_config
import pytest

from datakit_project import cookiecutters, Templates
from datakit_project import exceptions as dkit_exceptions


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

"""
@mock.patch.object('datakit_project.cookiecutters.Repository', 'info',
    return_value = {
          'Name': 'fake-repo',
          'SHA': 'a11706f',
          'Date': '2017-02-02',
          'Subject': 'Testing',
        }
)
"""
def test_network_unavailable(cookiecutter_home, deploy_template):
    deploy_template(cookiecutter_home, 'tests/fake-repo')

    error_message = (
        "fatal: unable to access 'https://github.com/associatedpress/fake-repo.git/': "
        "Could not resolve host: github.com"
    ).encode('utf-8')

    mock.patch(
        'datakit_project.repository.subprocess.check_output',
        autospec=True,
        side_effect=[subprocess.CalledProcessError(
            -1, 'cmd', output=error_message
        )]
    )

    with mock.patch('datakit_project.cookiecutters.Repository') as MockClass:
        instance = MockClass.return_value
        instance.info.return_value = {
          'Name': 'fake-repo',
          'SHA': 'a11706f',
          'Date': '2017-02-02',
          'Subject': 'Testing',
        }
        # Run the command
        with pytest.raises(dkit_exceptions.RepositoryFetchFailed) as err:
            parsed_args = mock.Mock()
            # Set status flag to true
            parsed_args.status = True
            cmd = Templates(None, None, cmd_name='project templates')
            cmd.run(parsed_args)
            assert 'Are you connected to a network?' in str(err.value)

