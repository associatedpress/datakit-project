import os
import subprocess


class Cookiecutters:

    def __init__(self, cookiecutters_dir):
        self.cookiecutters_dir = cookiecutters_dir

    def info(self):
        templates = os.listdir(self.cookiecutters_dir)
        repos_info = []
        cmd = ['git', 'log', '-n', '1', '--pretty=format:"%h\n%cd\n%s"', '--date=short']
        for template in templates:
            repo_dir = os.path.join(self.cookiecutters_dir, template)
            output = subprocess.check_output(
                cmd,
                cwd=repo_dir,
                stderr=subprocess.STDOUT
            )
            info = self._prepare_repo_info(template, output.decode().strip('"'))
            repos_info.append(info)
        return repos_info

    def _prepare_repo_info(self, template, info):
        sha1, commit_date, subject = info.split('\n')
        return {
            'Name': template,
            'sha1': sha1,
            'Date': commit_date,
            'Subject': subject
        }
