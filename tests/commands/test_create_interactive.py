import os
import re
import shutil
import subprocess
from unittest import mock

import pytest

from datakit_project import Create



#TODO: use parametrize with repo data for Cookiecutters
@pytest.mark.usefixtures('create_plugin_config_fake_repo')
def test_interactive_project_selection(caplog, cookiecutter_home, deploy_template, monkeypatch, tmpdir):
    deploy_template(cookiecutter_home, 'tests/fake-repo')
    deploy_template(cookiecutter_home, 'tests/fake-repo-two')
    # Set up the configs to point default template at our fake repo
    monkeypatch.chdir(tmpdir)
    with mock.patch('datakit_project.commands.create.Cookiecutters') as MockClass:
        instance = MockClass.return_value
        instance.list_templates.return_value = ['fake-repo', 'fake-repo-two']
        # Monkeypatch user selection
        monkeypatch.setattr(
            'datakit_project.commands.create.read_user_choice',
            lambda name, choices: 'fake-repo'
        )
        parsed_args = mock.Mock()
        parsed_args.make_default = False
        parsed_args.template = ''
        parsed_args.interactive = True
        # Use no_input to disable additional cookiecutter prompts
        parsed_args.no_input = True
        cmd = Create(None, None, cmd_name='project create')
        cmd.run(parsed_args)
        assert "Creating project from template: fake-repo" in caplog.text
