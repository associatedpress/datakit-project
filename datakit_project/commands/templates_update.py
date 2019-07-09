import argparse
import cookiecutter.config as cc_config
from cliff.command import Command

from .command_helpers import CommandHelpers
from .help_text import TEMPLATE_STATUS_MSG
from datakit_project.cookiecutters import Cookiecutters
from datakit_project.prompt import read_multichoice_or_all_input


class TemplatesUpdate(CommandHelpers, Command):
    "Update locally installed Cookiecutter templates"

    def get_parser(self, prog_name):
        parser = super(TemplatesUpdate, self).get_parser(prog_name)
        parser.formatter_class = argparse.RawTextHelpFormatter
        return parser

    def take_action(self, parsed_args):
        cc_home = cc_config.DEFAULT_CONFIG['cookiecutters_dir']
        cookiecutters = Cookiecutters(cc_home)
        templates = cookiecutters.info(status=True)
        out_of_date = [t for t in templates if t['commits_behind'] != 'Up-to-date']
        if len(out_of_date) == 0:
            self.log.info("Local templates are all up-to-date.\n")
            self.log.info(TEMPLATE_STATUS_MSG)
        else:
            self.log.info("The following template(s) are out of date:\n")
            choices = {}
            for idx, template in enumerate(out_of_date):
                option_num = str(idx + 1)
                choices[option_num] = template
                self.log.info("({}) {}\n".format(option_num, template['Name']))
            prompt_msg = (
                "Type one or more numbers for the templates you'd like to update, "
                "or type 'all'.\n"
            )
            response = read_multichoice_or_all_input(prompt_msg)
            if 'all' in response:
                to_update = sorted([temp['Name'] for temp in choices.values()])
                self.log.info("Updating all templates...")
            else:
                to_update = [choices[num]['Name'] for num in response]
                self.log.info("Updating selected templates...")
            cookiecutters.update(to_update)
