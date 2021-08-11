import argparse
from cliff.command import Command
from cookiecutter.main import cookiecutter
from cookiecutter.prompt import read_user_choice
from cookiecutter.exceptions import OutputDirExistsException
import cookiecutter.config as cc_config

from .command_helpers import CommandHelpers
from .help_text import CREATE_HELP_MSG, NO_TEMPLATES_ERROR_WITH_HELP_MSG
from datakit_project.cookiecutters import Cookiecutters
from datakit_project.utils import resolve_repo_dir


class Create(CommandHelpers, Command):
    """Create a new project."""

    def get_epilog(self):
        return CREATE_HELP_MSG

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        parser.formatter_class = argparse.RawTextHelpFormatter
        parser.add_argument(
            '-t',
            '--template',
            default='',
            help="Local path/Github URL for a Cookiecutter template"
        )
        parser.add_argument(
            '-d',
            '--make-default',
            action='store_true',
            default=False,
            help="Make the template the default for new projects"
        )
        parser.add_argument(
            '-i',
            '--interactive',
            action='store_true',
            default=False,
            help="enter interactive mode to choose a project template"
        )
        parser.add_argument(
            '-n',
            '--no-input',
            action='store_true',
            default=False,
            help="Whether to allow user input for Cookiecutter execution"
        )
        parser.add_argument(
            '-o',
            '--overwrite-if-exists',
            action='store_true',
            default=False,
            help="Whether to overwrite a directory with the same name as project slug or exit gracefully"
        )
        return parser

    def take_action(self, parsed_args):
        if parsed_args.interactive and parsed_args.template == '':
            cc_home = cc_config.DEFAULT_CONFIG['cookiecutters_dir']
            cc = Cookiecutters(cc_home)
            templates = cc.list_templates()
            template = read_user_choice('project template', templates)
        else:
            # Create project skeleton
            template = self.get_template(parsed_args)
        if template:
            self.log.info("Creating project from template: {}".format(template))
            try:
                cookiecutter(
                    template,
                    no_input=parsed_args.no_input,
                    overwrite_if_exists=parsed_args.overwrite_if_exists
                )
                repo_dir = resolve_repo_dir(template)
                # Update default template if it's empty or specifically requested
                if self.default_template == '' or parsed_args.make_default:
                    self.update_configs({'default_template': repo_dir})
                    tmplt_msg = "Set default template to {} in plugin config ({})".format(
                        repo_dir,
                        self.plugin_config_path
                    )
                    self.log.info(tmplt_msg)
            except OutputDirExistsException:
                msg = (
                    "Error: A project with the slug you provided already "
                    "exists in this directory. Try again with a different slug."
                )
                self.log.info(msg)
        else:
            self.log.info(NO_TEMPLATES_ERROR_WITH_HELP_MSG)
