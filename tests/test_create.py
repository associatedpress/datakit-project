from unittest import mock

import cookiecutter.config as cc_config

from datakit_project import Create


def test_warning_when_no_default_repo(caplog, monkeypatch, tmpdir):
    monkeypatch.setitem(
        cc_config.DEFAULT_CONFIG,
        'cookiecutters_dir',
        tmpdir
    )
    cmd = Create(None, None, cmd_name='project:create')
    parsed_args = mock.Mock()
    parsed_args.template = ''
    cmd.run(parsed_args)
    msg = 'No project templates have been installed'
    assert msg in caplog.text


"""
def test_create_with_no_previously_loaded_template(monkeypatch, tmpdir):
    parsed_args = mock.Mock()
    parsed_args.template = "fake-repo"
    monkeypatch.setitem(
        cookiecutter.config.DEFAULT_CONFIG,
        'cookiecutters_dir',
        tmpdir
    )
    cmd = Create(None, None, cmd_name='project:create')
    # Change working directory to tmp dir
    # tmpdir.chdir()
    # parsed_args.template = 'tests/fake-repo/'
    # TODO: should raise MissingTemplateError
    with pytest.raises(cookiecutter.exceptions.RepositoryNotFound):
        cmd.run(parsed_args)
        assert tmpdir.listdir() == expected
        cookiecutter_dir = tmpdir.join('.cookiecutter')
"""
