import os
import sys

from cement.core.controller import CementBaseController, expose
from datakit.plugins.project import Project, ProjectExistsError, InvalidProjectName


class ProjectController(CementBaseController):

    class Meta:
        label = 'project'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "CRUD operations for a project (create, destroy, etc.)"
        arguments = [
            (['name'], dict(action='store')),
            # TODO: optional argument for project
            #   directory; default to current working directory
        ]
        default_dirs = ['analysis', 'config', 'data', 'etl', 'lib']

    @expose(aliases=['c'], help="Create a new data project.")
    def create(self):
        # msg = "Creating project: {}".format(self.app.pargs.name)
        # self.app.log.info(msg)
        # TODO: proj name should be slug with dashes
        name = self.app.pargs.name
        try:
            self.app.log.info("Creating project: {}...".format(name))
            #proj = Project()
        except ProjectExistsError:
            sys.exit("Project {} already exists.".format(name))
        except InvalidProjectName:
            sys.exit("Project name ({}) is not valid.".format(name))

    @expose(aliases=['d'], help="Destroy a project.")
    def destroy(self):
        name = self.app.pargs.name
        self.app.log.info("Destroying project: {}".format(name))
        #self.app.project.destroy()
