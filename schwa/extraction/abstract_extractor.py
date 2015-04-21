# Copyright (c) 2015 Faculty of Engineering of the University of Porto
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

""" Module for representing Extractors Abstract classes.

If someone wants to add support to a new type of repository e.g. SVN,
it should start here.
"""
import abc
import re


class AbstractExtractor:
    """ An abstract class for a Repository Extractor.

    This class ensures that all the extractors have a pattern.

    Attributes:
        path: A String representing the local repository path
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, path):
        self.path = path

    @abc.abstractmethod
    def extract(self, ignore_regex="^$", max_commits=None):
        """ Extracts all the Java commits"""


def is_code_file(path):
    result = re.search(".+\.(java|php|py|cpp|c|js|html|css|rb|h|scala|sbt|sh|sql|cs)$", path)
    return result


def can_parse_file(path):
    result = re.search(".+\.(java)$", path)
    return result