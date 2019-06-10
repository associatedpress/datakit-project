import os

import cookiecutter.config as cc_config
from cliff.command import Command
from cookiecutter.main import cookiecutter

from .command_helpers import CommandHelpers
from .help_text import NO_TEMPLATES_ERROR_WITH_HELP_MSG, TEMPLATE_USAGE_MSG
from .utils import resolve_repo_dir


class Templates(CommandHelpers, Command):
    "List project templates"

    def get_parser(self, prog_name):
        parser = super(Templates, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        cc_home = cc_config.DEFAULT_CONFIG['cookiecutters_dir']
        templates = sorted(os.listdir(cc_home))
        self.log.info("\nCookiecutters directory: {}\n".format(cc_home))
        if len(templates) == 0:
            self.log.info(NO_TEMPLATES_ERROR_WITH_HELP_MSG)
        else:
            msg = ""
            for template in templates:
                msg += "\t- {}\n".format(template)
            msg += "\n" + TEMPLATE_USAGE_MSG
            self.log.info(msg)

