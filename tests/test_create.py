import os
from unittest import mock

from datakit_project import Create

def test_project_creation(tmpdir):
    parsed_args = mock.Mock()
    parsed_args.name = "test project"
    cmd = Create(None, None, cmd_name='project:create')
    expected = ['analysis', 'config', 'data', 'etl']
    # Change working directory to tmp dir
    tmpdir.chdir()
    cmd.run(parsed_args)
    assert tmpdir.listdir() == expected
