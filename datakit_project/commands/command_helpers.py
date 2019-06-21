import logging
import os

from datakit.utils import (
    home_dir,
    mkdir_p,
    read_json,
    write_json
)


class CommandHelpers:

    "Base class containing common helper methods for Cliff Command instances"

    log = logging.getLogger(__name__)

    def get_template(self, parsed_args):
        if parsed_args.template != '':
            return parsed_args.template
        else:
            return self.default_template

    def update_configs(self, new_configs):
        configs = self.configs
        configs.update(new_configs)
        self.write_configs(configs)
        return configs

    def write_configs(self, configs):
        mkdir_p(self.plugin_config_parent_dir)
        write_json(self.plugin_config_path, configs)

    @property
    def configs(self):
        try:
            configs = read_json(self.plugin_config_path)
        except FileNotFoundError:
            configs = self.default_configs
            self.write_configs(configs)
        return configs

    @property
    def plugin_config_parent_dir(self):
        return os.path.join(
            home_dir(),
            'plugins/datakit-project'
        )

    @property
    def plugin_config_path(self):
        return os.path.join(
            self.plugin_config_parent_dir,
            'config.json'
        )

    @property
    def default_configs(self):
        return {'default_template': ''}

    @property
    def default_template(self):
        try:
            return self.configs['default_template']
        except KeyError:
            msg = "ERROR: The 'default_template' setting is missing from" +\
                "your config file! {}".format(self.plugin_config_path)
            self.log.info(msg)
