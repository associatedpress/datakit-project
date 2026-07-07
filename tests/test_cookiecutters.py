import os
from unittest import mock

import pytest

from datakit_project.cookiecutters import Cookiecutters


@pytest.fixture
def templates_dir(tmpdir):
    root = tmpdir.mkdir('cookiecutters')
    for name in ('fake-repo', 'fake-repo-two'):
        root.mkdir(name)
    return str(root)


def test_list_templates(templates_dir):
    cookiecutters = Cookiecutters(templates_dir)
    assert sorted(cookiecutters.list_templates()) == ['fake-repo', 'fake-repo-two']


def test_info_without_status(templates_dir, monkeypatch):
    def fake_info(self):
        return {'Name': self.path.name}

    monkeypatch.setattr('datakit_project.repository.Repository.info', fake_info)
    cookiecutters = Cookiecutters(templates_dir)
    names = sorted(repo['Name'] for repo in cookiecutters.info())
    assert names == ['fake-repo', 'fake-repo-two']


def test_info_skips_unreadable_repos(templates_dir, monkeypatch):
    def fake_info(self):
        if self.path.name == 'fake-repo-two':
            raise OSError('not a repo')
        return {'Name': self.path.name}

    monkeypatch.setattr('datakit_project.repository.Repository.info', fake_info)
    cookiecutters = Cookiecutters(templates_dir)
    assert [repo['Name'] for repo in cookiecutters.info()] == ['fake-repo']


def test_info_with_status_marks_uptodate(templates_dir, monkeypatch):
    monkeypatch.setattr(
        'datakit_project.repository.Repository.info',
        lambda self: {'Name': self.path.name},
    )
    monkeypatch.setattr(
        'datakit_project.repository.Repository.fetch', lambda self: None
    )
    monkeypatch.setattr(
        'datakit_project.repository.Repository.upstream_info',
        lambda self: {'commits_behind': 0},
    )
    cookiecutters = Cookiecutters(templates_dir)
    info = cookiecutters.info(status=True)
    assert all(repo['commits_behind'] == 'Up-to-date' for repo in info)


def test_info_with_status_preserves_behind_count(templates_dir, monkeypatch):
    monkeypatch.setattr(
        'datakit_project.repository.Repository.info',
        lambda self: {'Name': self.path.name},
    )
    monkeypatch.setattr(
        'datakit_project.repository.Repository.fetch', lambda self: None
    )
    monkeypatch.setattr(
        'datakit_project.repository.Repository.upstream_info',
        lambda self: {'commits_behind': 4},
    )
    cookiecutters = Cookiecutters(templates_dir)
    info = cookiecutters.info(status=True)
    assert all(repo['commits_behind'] == 4 for repo in info)


def test_update_pulls_each_named_template(templates_dir):
    with mock.patch('datakit_project.cookiecutters.Repository') as MockRepo:
        cookiecutters = Cookiecutters(templates_dir)
        cookiecutters.update(['fake-repo', 'fake-repo-two'])
    called_dirs = [call.args[0] for call in MockRepo.call_args_list]
    assert called_dirs == [
        os.path.join(templates_dir, 'fake-repo'),
        os.path.join(templates_dir, 'fake-repo-two'),
    ]
    assert MockRepo.return_value.update.call_count == 2
