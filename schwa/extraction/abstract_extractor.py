import abc
import re


class AbstractExtractor:
    __metaclass__ = abc.ABCMeta

    def __init__(self, path):
        self.path = path

    @abc.abstractmethod
    def extract(self, ignore_regex="^$", max_commits=None):
        """ extracts all the necessary commits"""


def is_code_file(path):
    result = re.search(".+\.(java|php|py|cpp|c|js|html|css|rb|h)", path)
    return result