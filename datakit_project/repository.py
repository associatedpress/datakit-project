import subprocess

from pathlib import Path

from datakit_project.exceptions import RepositoryFetchFailed


class Repository:

    def __init__(self, path):
        self.path = Path(path)

    def info(self):
        cmd = self._log_pretty_cmd()
        output = self._syscall(cmd)
        return self._prepare_repo_info(output.strip('"'))

    def upstream_info(self):
        cmd = self._log_pretty_cmd()
        cmd.append(
            self.upstream_tracking_branch
        )
        output = self._syscall(cmd)
        info = self._prepare_repo_info(output.strip('"'))
        return {
            'upstream_sha': info['SHA'],
            'upstream_date': info['Date'],
            'upstream_subject': info['Subject'],
            'commits_behind': self.commits_behind_upstream,
        }

    def update(self):
        remote, branch = self.upstream_tracking_branch.split('/')
        cmd = ['git', 'pull', remote, branch]
        self._syscall(cmd)

    @property
    def local_branch(self):
        cmd = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
        return self._syscall(cmd)

    @property
    def upstream_tracking_branch(self):
        cmd = ['git', 'rev-parse', '--abbrev-ref', 'HEAD@{upstream}']
        return self._syscall(cmd)

    @property
    def commits_behind_upstream(self):
        cmd = ['git', 'rev-list', '--count', "{}..{}".format(
            self.local_branch,
            self.upstream_tracking_branch
        )]
        return int(self._syscall(cmd))

    def fetch(self):
        cmd = ['git', 'fetch']
        self._syscall(cmd)

    def _log_pretty_cmd(self):
        cmd = ['git', 'log', '-n', '1', '--pretty=format:"%h\n%cd\n%s"', '--date=short']
        return cmd

    def _prepare_repo_info(self, info):
        sha1, commit_date, subject = info.split('\n')
        return {
            'Name': self.path.name,
            'SHA': sha1,
            'Date': commit_date,
            'Subject': subject
        }

    def _syscall(self, cmd):
        try:
            output = subprocess.check_output(
                cmd,
                cwd=str(self.path),
                stderr=subprocess.STDOUT
            ).decode().strip()
            return output
        except subprocess.CalledProcessError as git_error:
            output = git_error.output.decode('utf-8')
            if 'fatal: unable to access' in output:
                msg = [output.split("fatal:")[1].strip()]
                msg.append("Are you connected to a network?")
                final = "\n".join(msg)
                raise RepositoryFetchFailed(final)
