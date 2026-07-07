import subprocess

import pytest

from datakit_project.exceptions import (
    RepositoryCommandFailed,
    RepositoryFetchFailed,
)
from datakit_project.repository import Repository


@pytest.fixture
def repo():
    return Repository('/path/to/fake-repo')


def stub_syscalls(monkeypatch, repo, responses):
    """Replace _syscall with a lookup keyed on the command that runs it."""
    def _syscall(cmd):
        return responses[tuple(cmd)]
    monkeypatch.setattr(repo, '_syscall', _syscall)


def test_info(monkeypatch, repo):
    stub_syscalls(monkeypatch, repo, {
        tuple(repo._log_pretty_cmd()): '"abc1234\n2020-01-01\nInitial commit"',
    })
    assert repo.info() == {
        'Name': 'fake-repo',
        'SHA': 'abc1234',
        'Date': '2020-01-01',
        'Subject': 'Initial commit',
    }


def test_upstream_info(monkeypatch, repo):
    upstream_log_cmd = tuple(repo._log_pretty_cmd() + ['origin/master'])
    stub_syscalls(monkeypatch, repo, {
        ('git', 'rev-parse', '--abbrev-ref', 'HEAD@{upstream}'): 'origin/master',
        upstream_log_cmd: '"def5678\n2020-02-02\nUpstream commit"',
        ('git', 'rev-parse', '--abbrev-ref', 'HEAD'): 'main',
        ('git', 'rev-list', '--count', 'main..origin/master'): '3',
    })
    assert repo.upstream_info() == {
        'upstream_sha': 'def5678',
        'upstream_date': '2020-02-02',
        'upstream_subject': 'Upstream commit',
        'commits_behind': 3,
    }


def test_update_splits_remote_and_branch(monkeypatch, repo):
    calls = []
    monkeypatch.setattr(repo, '_syscall', lambda cmd: calls.append(cmd))
    monkeypatch.setattr(
        Repository, 'upstream_tracking_branch', 'origin/feature/x'
    )
    repo.update()
    assert calls == [['git', 'pull', 'origin', 'feature/x']]


def test_fetch(monkeypatch, repo):
    calls = []
    monkeypatch.setattr(repo, '_syscall', lambda cmd: calls.append(cmd))
    repo.fetch()
    assert calls == [['git', 'fetch']]


def test_cached_branch_lookups_run_once(monkeypatch, repo):
    calls = []

    def _syscall(cmd):
        calls.append(cmd)
        return 'main'

    monkeypatch.setattr(repo, '_syscall', _syscall)
    assert repo.local_branch == 'main'
    assert repo.local_branch == 'main'
    assert calls == [['git', 'rev-parse', '--abbrev-ref', 'HEAD']]


def test_syscall_returns_stripped_output(monkeypatch, repo):
    monkeypatch.setattr(
        subprocess, 'check_output',
        lambda cmd, cwd, stderr: b'  some output\n'
    )
    assert repo._syscall(['git', 'status']) == 'some output'


def test_syscall_raises_fetch_failed_on_network_error(monkeypatch, repo):
    def boom(cmd, cwd, stderr):
        raise subprocess.CalledProcessError(
            128, cmd,
            output=b"fatal: unable to access 'https://example.com/': timeout",
        )

    monkeypatch.setattr(subprocess, 'check_output', boom)
    with pytest.raises(RepositoryFetchFailed) as excinfo:
        repo._syscall(['git', 'fetch'])
    assert 'Are you connected to a network?' in str(excinfo.value)


def test_syscall_raises_command_failed_on_other_errors(monkeypatch, repo):
    def boom(cmd, cwd, stderr):
        raise subprocess.CalledProcessError(
            1, cmd, output=b'fatal: not a git repository',
        )

    monkeypatch.setattr(subprocess, 'check_output', boom)
    with pytest.raises(RepositoryCommandFailed) as excinfo:
        repo._syscall(['git', 'log'])
    assert 'not a git repository' in str(excinfo.value)
