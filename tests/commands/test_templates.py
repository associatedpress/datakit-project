from unittest import mock

from datakit_project import Templates


def test_no_templates(caplog, cookiecutter_home):
    """
    Templates should point the user at install help when no cookiecutters exist.
    """
    cmd = Templates(None, None)
    cmd.run(mock.Mock(status=False))
    assert cookiecutter_home in caplog.text
    assert "No project templates have been installed!" in caplog.text


def test_multiple_templates(caplog, log_lines):
    """
    Templates should render installed cookiecutters as a table sorted by name.
    """
    with mock.patch('datakit_project.commands.command_helpers.Cookiecutters') as MockClass:
        MockClass.return_value.info.return_value = [
            {'Name': 'fake-repo', 'SHA': 'a11706f', 'Date': '2017-02-02', 'Subject': 'Testing'},
            {'Name': 'fake-repo-two', 'SHA': '55f62a0', 'Date': '2019-03-06', 'Subject': 'Testing'},
        ]
        cmd = Templates(None, None)
        cmd.run(mock.Mock(status=False))
    expected = [
        "Name            SHA       Date         Subject",
        "fake-repo       a11706f   2017-02-02   Testing",
        "fake-repo-two   55f62a0   2019-03-06   Testing",
    ]
    lines = log_lines(caplog)
    assert all(row in lines for row in expected)
    # Header first, then rows in name-sorted order.
    positions = [lines.index(row) for row in expected]
    assert positions == sorted(positions)
