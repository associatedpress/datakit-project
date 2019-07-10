import os

from .repository import Repository


class Cookiecutters:

    def __init__(self, cookiecutters_dir):
        self.cookiecutters_dir = cookiecutters_dir

    def info(self, status=False):
        repos_info = []
        for template in self.list_templates():
            repo_dir = os.path.join(self.cookiecutters_dir, template)
            repo = Repository(repo_dir)
            data = repo.info()
            if status:
                repo.fetch()
                upstream = repo.upstream_info()
                if upstream['commits_behind'] == 0:
                    upstream['commits_behind'] = 'Up-to-date'
                data.update(upstream)
            repos_info.append(data)
        return repos_info

    def update(self, templates=[]):
        for template in templates:
            repo_dir = os.path.join(self.cookiecutters_dir, template)
            repo = Repository(repo_dir)
            repo.update()

    def list_templates(self):
        return os.listdir(self.cookiecutters_dir)
