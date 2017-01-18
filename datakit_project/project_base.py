import logging
import json
import os

import datakit.utils

from .utils import read_json, write_json


class ProjectBase:

    "Base class containing common helper methods, attributes"

    log = logging.getLogger(__name__)

    def get_template(self, parsed_args):
        if parsed_args.template != '':
            return parsed_args.template
        else:
            return self.default_template

    def update_configs(self, opts):
        configs = self.configs
        configs.update(opts)
        write_json(self.plugin_config_path, configs)

    @property
    def configs(self):
        return read_json(self.plugin_config_path)

    @property
    def plugin_config_path(self):
        return os.path.join(
            datakit.utils.home_dir(),
            'plugins/datakit-project/config.json'
        )

    @property
    def default_template(self):
        try:
            return self.configs['default_template']
        except KeyError:
            msg = "ERROR: The 'default_template' setting is missing from" +\
                "your config file! {}".format(self.plugin_config_path)
            self.log.info(msg)
