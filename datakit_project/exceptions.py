
class RepositoryFetchFailed(Exception):
    """
    Raised when upstream Git repo cannot be reached.
    """


class RepositoryCommandFailed(Exception):
    """
    Raised when a git command fails for a reason other than network access.
    """


class UnsupportedRepoType(Exception):
    """
    Raised when a template URL can't be classified as a git or hg repo.
    """
