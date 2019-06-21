import os


import cookiecutter.config as cc_config
import pytest

from datakit_project.utils import resolve_repo_dir


# TODO: Update resolve_repo_dir to use cookiecutter DEFAULT_CONFIG
# then monkeypatch the variable here
def test_repo_dir_for_local_repo():
    """
    Should be fully-qualified path to local directory
    """
    local_dir = '/Local/path/to/fake-repo'
    actual_dir = resolve_repo_dir(local_dir)
    assert local_dir == actual_dir


def test_repo_dir_for_alias():
    """
    Should be path inside of cookiecutter's dir.
    """
    cc_home = cc_config.DEFAULT_CONFIG['cookiecutters_dir']
    expected_dir = os.path.join(cc_home, 'fake-repo')
    actual_dir = resolve_repo_dir('gh:associatedpress/fake-repo')
    assert expected_dir == actual_dir


def test_repo_dir_for_url():
    """
    Should be path inside of cookiecutter's dir.
    """
    cc_home = cc_config.DEFAULT_CONFIG['cookiecutters_dir']
    expected_dir = os.path.join(cc_home, 'fake-repo')
    actual_dir = resolve_repo_dir('https://github.com/associatedpress/fake-repo.git')
    assert expected_dir == actual_dir
