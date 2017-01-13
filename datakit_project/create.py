import logging

from cookiecutter.main import cookiecutter
from cliff.command import Command


class Create(Command):
    "Create a new project"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        # NOTE: optional by default
        parser.add_argument(
            'template',
            default='',
            help="Local path/Github URL for a Cookiecutter template"
        )
        # TODO: parser.add_argument(
        #    '--make-default',
        # help="Make the template the default for new projects"
        # )
        return parser

    def take_action(self, parsed_args):
        # Create project skeleton
        template = self._get_template(parsed_args)
        if template:
            self.log.info("Creating project: {}".format(parsed_args.template))
            cookiecutter(
                template,
                overwrite_if_exists=True,
            )
        else:
            msg = 'No project templates have been installed. You must ' +\
                'specify the local path or URL to a Cookiecutter project repo'
            msg2 = "foobar"
            self.log.info(msg)
            print(msg)
        # TODO: if parserd_args.make_default, update ~/.datakit/plugins/datakit_project.json
        # TODO: if datakit-vcs plugin, call it's bootstrap method
        # TODO: if project_management (i.e. Gitlab), call it's bootstrap method
        return parsed_args.name

    # PRIVATE

    def _get_template(self, parsed_args):
        if parsed_args.template != '':
            return parsed_args.template
        else:
            return self._default_template

    @property
    def _default_template(self):
        # TODO: Get cookiecutter home directory using Cookiecutter API and check
        # the plugin's config file .../.datakit/plugins/datakit_project.json for the 
        # default_template setting
        pass
