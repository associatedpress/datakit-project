from cliff.command import Command
from cookiecutter.main import cookiecutter

from .command_helpers import CommandHelpers
from .utils import resolve_repo_dir


class Create(CommandHelpers, Command):
    "Create a new project"

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
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
            '--no-input',
            action='store_true',
            default=False,
            help="Disable prompts for CLI input"
        )
        return parser

    def take_action(self, parsed_args):
        # Create project skeleton
        template = self.get_template(parsed_args)
        if template:
            self.log.info("Creating project from template: {}".format(template))
            cookiecutter(
                template,
                overwrite_if_exists=True,
                no_input=parsed_args.no_input
            )
            repo_dir = resolve_repo_dir(template)
            # Update default template if it's empty or specifically requested
            if self.default_template == '' or parsed_args.make_default:
                self.update_configs({'default_template': repo_dir})
                tmplt_msg = "Set default template to {} in plugin config ({})".format(repo_dir, self.plugin_config_path)
                self.log.info(tmplt_msg)
        else:
            error_msg = 'No project templates have been installed. ' +\
                'You must specify the local path or URL to a ' +\
                'Cookiecutter project repo.'
            self.log.info(error_msg)
