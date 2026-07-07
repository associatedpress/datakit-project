from unittest import mock

import pytest

from datakit_project import Templates


def _repo(name, sha, date, up_sha, up_date, behind):
    return {
        'Name': name, 'SHA': sha, 'Date': date, 'Subject': 'Testing',
        'upstream_sha': up_sha, 'upstream_date': up_date,
        'upstream_subject': 'Testing', 'commits_behind': behind,
    }


HEADER = "Name            SHA       Date         Upstream SHA   Upstream Date   Commits behind"


@pytest.mark.parametrize('info, rows', [
    pytest.param(
        [
            _repo('fake-repo', 'a11706f', '2017-02-02', 'a11706f', '2017-02-02', 'Up-to-date'),
            _repo('fake-repo-two', '55f62a0', '2019-03-06', '55f62a0', '2019-03-06', 'Up-to-date'),
        ],
        [
            "fake-repo       a11706f   2017-02-02   a11706f        2017-02-02      Up-to-date",
            "fake-repo-two   55f62a0   2019-03-06   55f62a0        2019-03-06      Up-to-date",
        ],
        id='all-up-to-date',
    ),
    pytest.param(
        [
            _repo('fake-repo', 'a11706f', '2017-02-02', 'c18705e', '2017-06-01', 3),
            _repo('fake-repo-two', '55f62a0', '2019-03-06', '55f62a0', '2019-03-06', 'Up-to-date'),
        ],
        [
            "fake-repo       a11706f   2017-02-02   c18705e        2017-06-01      3",
            "fake-repo-two   55f62a0   2019-03-06   55f62a0        2019-03-06      Up-to-date",
        ],
        id='one-behind-upstream',
    ),
])
def test_status_table(info, rows, caplog, log_lines):
    """
    `templates --status` should render the upstream comparison, showing the
    commits-behind count and sorting rows by template name.
    """
    with mock.patch('datakit_project.commands.command_helpers.Cookiecutters') as MockClass:
        MockClass.return_value.info.return_value = info
        cmd = Templates(None, None)
        cmd.run(mock.Mock(status=True))
    lines = log_lines(caplog)
    expected = [HEADER, *rows]
    assert all(line in lines for line in expected)
    positions = [lines.index(line) for line in expected]
    assert positions == sorted(positions)
