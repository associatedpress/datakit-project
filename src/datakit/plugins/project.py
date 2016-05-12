import os
import shutil

from datakit.utils import makedirs


class ProjectExistsError(Exception):
    pass


class InvalidProjectName(Exception):
    # TODO: Customize message to include details on
    #   valid naming convention
    pass


class Project:

    def __init__(self, path=os.getcwd(), subdirs=[], files={}):
        self.path = path
        self.subdirs = subdirs
        self.files = files

    # ~~~ PUBLIC ~~~

    def create(self):
        try:
            os.mkdir(self.path)
        # Use OSError for 2.7 backwards-compatability, if we go there
        except OSError:
            msg = "{} already exists!!".format(self.path)
            raise ProjectExistsError(msg)
        except TypeError:
            msg = "No path provided!"
            raise InvalidProjectName(msg)
        makedirs(self.path, self.subdirs)

    def destroy(self):
        shutil.rmtree(self.path)

    # ~~~ PRIVATE ~~~

    # TODO: Implement project name validation
    def __valid_name(self):
        pass
