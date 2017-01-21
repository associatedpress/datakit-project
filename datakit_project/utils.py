import os
import errno
import json
import re

from cookiecutter.config import BUILTIN_ABBREVIATIONS, DEFAULT_CONFIG
from cookiecutter.repository import expand_abbreviations, is_repo_url
from cookiecutter.vcs import identify_repo


def read_json(path):
    with open(path) as fh:
        return json.load(fh)


def write_json(path, data):
    with open(path, 'w') as fh:
        json.dump(data, fh)


def mkdir_p(directory_name):
    try:
        os.makedirs(directory_name)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(directory_name):
            pass
        else:
            raise


def resolve_repo_dir(template):
    """
    Determine path to local repository based on template name.
    This can be either a local path, a remote URL or a remote alias
    such as for Github.

    Sundry bits from Cookiecutter do the heavy lifting here.

    Arguments

      template [path|url|alias]

    """
    cc_home = DEFAULT_CONFIG['cookiecutters_dir']
    if template_type(template) in ['remote alias', 'url']:
        raw_url = expand_abbreviations(template, BUILTIN_ABBREVIATIONS)
        repo_type, repo_url = identify_repo(raw_url)
        repo_url = repo_url.rstrip('/')
        tail = os.path.split(repo_url)[1]
        if repo_type == 'git':
            repo_dir = os.path.normpath(os.path.join(cc_home,
                                                     tail.rsplit('.git')[0]))
        elif repo_type == 'hg':
            repo_dir = os.path.normpath(os.path.join(cc_home, tail))
            repo_dir = template
    else:
        repo_dir = os.path.abspath(template)
    return repo_dir


def template_type(template):
    status = 'local directory'
    if re.match(r'(gh|hg):', template):
        status = 'remote alias'
    if is_repo_url(template):
        status = 'url'
    return status
