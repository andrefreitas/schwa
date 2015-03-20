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

""" Module for the Git Extractor. """

import multiprocessing
import git
from .abstract_extractor import *
from schwa.repository import *
from schwa.parsing import JavaParser

current_repo = None  # Curent repository wrapper


def extract_commit_wrapper(hexsha):
    """ Multiprocessing wrapper for extracting a commit"""
    return current_repo.extract_commit(hexsha)


class GitExtractor(AbstractExtractor):
    """ A Git Extractor.

    This class relies on GitPython library to extract data from a local repository.
    """

    def __init__(self, path):
        super().__init__(path)
        self.repo = git.Repo(path, odbt=git.GitCmdObjectDB)

    def extract(self, ignore_regex="^$", max_commits=None, method_granularity=False, parallel=True):
        """ Extract a repository.

        It extracts commits from a repository that are important to the analysis. Therefore, only commits
        related to code are important. For the sake of supporting big repositories, it is possible to set
        the maximum number of commits.

        Args:
            ignore_regex: An optional string that is a regex pattern to ignore unnecessary files.
            max_commits: An optional int that is the maximum number of commits to extract since the last one.
            method_granularity: An optional boolean that enables extraction until the method granularity.
            parallel: An optional boolean that enables multiprocessing extraction.

        Returns:
            A Repository instance.
        """

        # Multiprocessing setup
        global current_repo
        current_repo = self
        try:
            cpus = multiprocessing.cpu_count()
        except NotImplementedError:  # pragma: no cover
            cpus = 2   # pragma: no cover
        self.ignore_regex = ignore_regex
        self.method_granularity = method_granularity

        # Extract commits
        iter_commits = self.repo.iter_commits(max_count=max_commits) if max_commits else self.repo.iter_commits()
        commits = [commit.hexsha for commit in iter_commits]
        pool = multiprocessing.Pool(processes=cpus)
        if parallel:
            commits = pool.map(extract_commit_wrapper, commits)
        else:
            commits = map(extract_commit_wrapper, commits)
        commits = list(reversed([commit for commit in commits if commit]))

        # Timestamps
        begin_ts = list(self.repo.iter_commits())[-1].committed_date
        last_ts = list(self.repo.iter_commits(max_count=1))[0].committed_date

        # Repository
        repo = Repository(commits, begin_ts, last_ts)
        return repo

    def extract_commit(self, hexsha):
        """ Extract a commit.

        Iterates over commits diffs to extract important information such as changed files, classes and methods.

        Args:
            hexsha: A string representing the commit ID

        Returns:
            A Commit instance.
        """
        commit = self.repo.commit(hexsha)
        try:
            _id = hexsha
            message = commit.message
            author = commit.author.email
            timestamp = commit.committed_date
            diffs_list = []
            is_good_blob = lambda blob: blob and is_code_file(blob.path) and not re.search(self.ignore_regex, blob.path)
            # print("extracting", _id, message)

            # If it's first commit
            if not commit.parents:
                blobs = commit.tree.traverse()
                for blob in blobs:
                    if is_good_blob(blob):
                        diffs_list.append(DiffFile(file_b=blob.path, added=True))
                        if self.method_granularity:
                            source = blob.data_stream.read().decode("UTF-8")
                            components = GitExtractor.parse(blob.path, source)
                            for _, _, c, f in components:  # Iterates over methods
                                diffs_list.append(DiffMethod(file_name=blob.path, class_name=c, method_b=f, added=True))
                            for c in set(c for _, _, c, f in components):  # Iterates over classes
                                diffs_list.append(DiffClass(file_name=blob.path, class_b=c, added=True))

            for parent in commit.parents:
                diffs = parent.diff(commit)
                for diff in diffs:
                    if not is_good_blob(diff.a_blob) and not is_good_blob(diff.b_blob):
                        continue
                    if diff.new_file:
                        diffs_list.append(DiffFile(file_b=diff.b_blob.path, added=True))
                        if self.method_granularity:
                            source = diff.b_blob.data_stream.read().decode("UTF-8")
                            components = GitExtractor.parse(diff.b_blob.path, source)
                            for _, _, c, f in components:
                                diffs_list.append(DiffMethod(file_name=diff.b_blob.path, class_name=c, method_b=f, added=True))
                            for c in set(c for _, _, c, f in components):
                                diffs_list.append(DiffClass(file_name=diff.b_blob.path, class_b=c, added=True))
                    elif diff.renamed:
                        if is_good_blob(diff.b_blob):
                            diffs_list.append(DiffFile(file_a=diff.rename_from, file_b=diff.rename_to, renamed=True))
                            if self.method_granularity:
                                source_a = diff.a_blob.data_stream.read().decode("UTF-8")
                                source_b = diff.b_blob.data_stream.read().decode("UTF-8")
                                diffs_list.extend(GitExtractor.diff((diff.rename_from, source_a), (diff.rename_to, source_b)))
                    elif diff.deleted_file:
                        diffs_list.append(DiffFile(file_a=diff.a_blob.path, removed=True))
                    else:
                        diffs_list.append(DiffFile(file_a=diff.a_blob.path, file_b=diff.b_blob.path, modified=True))
                        if self.method_granularity:
                            source_a = diff.a_blob.data_stream.read().decode("UTF-8")
                            source_b = diff.b_blob.data_stream.read().decode("UTF-8")
                            diffs_list.extend(GitExtractor.diff((diff.a_blob.path, source_a), (diff.b_blob.path, source_b)))

            return Commit(_id, message, author, timestamp, diffs_list) if len(diffs_list) > 0 else None

        except TypeError:  # pragma: no cover
            return None  # pragma: no cover
        except UnicodeDecodeError:  # pragma: no cover
            return None  # pragma: no cover
        except AttributeError:  # pragma: no cover
            return None  # pragma: no cover

    @staticmethod
    def parse(path, source):
        if "java" in path:
            components = JavaParser.parse(source)
            return components

    @staticmethod
    def diff(file_a, file_b):
        if "java" in file_a[0]:
            components_diff = JavaParser.diff(file_a, file_b)
            return components_diff