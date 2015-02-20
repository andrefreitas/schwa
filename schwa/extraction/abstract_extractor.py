import abc
import re


class AbstractExtractor:
    __metaclass__ = abc.ABCMeta

    def __init__(self, path, ignore_regex):
        self.path = path
        self.ignore_regex = ignore_regex

    @abc.abstractmethod
    def files(self):
        """ returns only code files e.g. .php, .java"""

    @abc.abstractmethod
    def commits(self):
        """ returns only commits that change code files """

    @abc.abstractmethod
    def timestamp(self):
        """ returns the timestamp of repository creation """



def is_code_file(path):
    result = re.search(".+\.(java|php|py|cpp|c|js|html|css|rb)", path)
    return result