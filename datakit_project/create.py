import logging
import json
import os

from cliff.command import Command
from cookiecutter.main import cookiecutter

from .command_helpers import CommandHelpers


class Create(CommandHelpers, Command):
    "Create a new project"

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        parser.add_argument(
            '--template',
            default='',
            help="Local path/Github URL for a Cookiecutter template"
        )
        parser.add_argument(
            '--no-input',
            default=False,
            help="Disable prompts for CLI input"
        )
        # TODO: parser.add_argument(
        #    '--make-default',
        # help="Make the template the default for new projects"
        # )
        return parser

    def take_action(self, parsed_args):
        # Create project skeleton
        template = self.get_template(parsed_args)
        if template:
            self.log.info("Creating project: {}".format(parsed_args.template))
            cookiecutter(
                template,
                overwrite_if_exists=True,
                no_input=parsed_args.no_input
            )
            # Update default template if it's empty or specifically requested
            if self.default_template == '':
                self.update_configs({'default_template': template})
                tmplt_msg = "Set default template to {} in plugin config ({})".format(template, self.plugin_config_path)
                self.log.info(tmplt_msg)
        else:
            error_msg = 'No project templates have been installed. ' +\
                'You must specify the local path or URL to a ' +\
                'Cookiecutter project repo.'
            self.log.info(error_msg)
        # TODO: if parserd_args.make_default, update ~/.datakit/plugins/datakit_project.json
        # TODO: if datakit-vcs plugin, call it's bootstrap method
        # TODO: if project_management (i.e. Gitlab), call it's bootstrap method
        return parsed_args.name
