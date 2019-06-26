import cookiecutter.config as cc_config
import prettytable as pt
from cliff.command import Command

from .command_helpers import CommandHelpers
from .help_text import NO_TEMPLATES_ERROR_WITH_HELP_MSG, TEMPLATE_USAGE_MSG
from datakit_project.cookiecutters import Cookiecutters


class Templates(CommandHelpers, Command):
    "List project templates"

    def get_parser(self, prog_name):
        parser = super(Templates, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        cc_home = cc_config.DEFAULT_CONFIG['cookiecutters_dir']
        cookiecutters = Cookiecutters(cc_home)
        templates = cookiecutters.info()
        self.log.info("\nLocal Cookiecutter templates ({}):\n".format(cc_home))
        if len(templates) == 0:
            self.log.info(NO_TEMPLATES_ERROR_WITH_HELP_MSG)
        else:
            fields = ('Name', 'SHA', 'Date', 'Subject')
            tbl = pt.PrettyTable(
                field_names=fields,
                border=False,
                hrules=pt.NONE,
                vrules=pt.NONE,
                left_padding_width=2,
                sortby='Name'
            )
            alignments = dict(zip(fields, len(fields) * ['l']))
            tbl.align.update(alignments)
            for row in templates:
                vals = (
                    row['Name'],
                    row['SHA'],
                    row['Date'],
                    row['Subject']
                )
                tbl.add_row(vals)
            self.log.info(tbl)
            self.log.info('\n')
            self.log.info(TEMPLATE_USAGE_MSG)
