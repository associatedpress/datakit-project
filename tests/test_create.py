from unittest import mock

from datakit_project import Create

def test_project_creation():
    parsed_args = mock.Mock()
    parsed_args.name = "Foobar"
    cmd = Create(None, None, cmd_name='project:create')
    assert cmd.run(parsed_args) == "Foobar"
