import argparse
import cookiecutter.config as cc_config
from cliff.command import Command

from .command_helpers import CommandHelpers
from .help_text import (
    NO_TEMPLATES_ERROR_WITH_HELP_MSG,
    TEMPLATE_USAGE_MSG,
    TEMPLATE_UPDATE_MSG
)
from datakit_project.cookiecutters import Cookiecutters
from datakit_project.formatters.templates import Templates as formatter


class Templates(CommandHelpers, Command):
    "List project templates"

    def get_parser(self, prog_name):
        parser = super(Templates, self).get_parser(prog_name)
        parser.formatter_class = argparse.RawTextHelpFormatter
        parser.add_argument(
            '-s',
            '--status',
            action='store_true',
            default=False,
            help="Check for updates on local Cookiecutter templates"
        )
        return parser

    def take_action(self, parsed_args):
        cc_home = cc_config.DEFAULT_CONFIG['cookiecutters_dir']
        cookiecutters = Cookiecutters(cc_home)
        templates = cookiecutters.info(status=parsed_args.status)
        self.log.info("\nLocal Cookiecutter templates ({}):\n".format(cc_home))
        if len(templates) == 0:
            self.log.info(NO_TEMPLATES_ERROR_WITH_HELP_MSG)
        else:
            if parsed_args.status:
                tbl = formatter.status(templates)
            else:
                tbl = formatter.list(templates)
            self.log.info(tbl)
            self.log.info('\n')
            self.log.info(TEMPLATE_USAGE_MSG)
            self.log.info(TEMPLATE_UPDATE_MSG)
