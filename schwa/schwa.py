""" Main entrypoint of Schwa library. """

from schwa import extraction


def analyze(repository_path, commits):
    extractor = extraction.Git(repository_path)
    repository = extractor.extract(commits)
