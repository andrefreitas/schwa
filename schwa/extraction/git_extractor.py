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
import os
import git
from .abstract_extractor import *
from schwa.repository import *
from schwa.parsing import JavaParser, ParsingError


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
        if parallel and os.name != "nt":
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
        _id = hexsha

        try:
            message = commit.message
        except UnicodeDecodeError:  # pragma: no cover
            return None  # pragma: no cover

        author = commit.author.email
        timestamp = commit.committed_date
        diffs_list = []

        # First commit
        if not commit.parents:
            for blob in commit.tree.traverse():
                if self.is_good_blob(blob):
                    diffs_list.extend(self.get_new_file_diffs(blob))
        else:
            for parent in commit.parents:
                for diff in parent.diff(commit):
                    # Shortcut
                    if not self.is_good_blob(diff.a_blob) and not self.is_good_blob(diff.b_blob):
                        continue
                    # New file
                    if diff.new_file and self.is_good_blob(diff.b_blob):
                        diffs_list.extend(self.get_new_file_diffs(diff.b_blob))
                    # Renamed file
                    elif diff.renamed and self.is_good_blob(diff.a_blob) and self.is_good_blob(diff.b_blob):
                        diffs_list.extend(self.get_renamed_file_diffs(diff.a_blob, diff.b_blob))
                    # Deleted file
                    elif diff.deleted_file:
                        diffs_list.append(DiffFile(file_a=diff.a_blob.path, removed=True))
                    # Modified file
                    else:
                        diffs_list.extend(self.get_modified_file_diffs(diff.a_blob, diff.b_blob))

        return Commit(_id, message, author, timestamp, diffs_list) if len(diffs_list) > 0 else None

    def get_new_file_diffs(self, blob):
        diffs_list = [DiffFile(file_b=blob.path, added=True)]
        if can_parse_file(blob.path) and self.method_granularity:
            source = GitExtractor.get_source(blob)
            file_parsed = GitExtractor.parse(blob.path, source)
            if file_parsed:
                classes_set = file_parsed.get_classes_set()
                methods_set = file_parsed.get_functions_set()
                for c in classes_set:
                    diffs_list.append(DiffClass(file_name=blob.path, class_b=c, added=True))
                for c, m in methods_set:
                    diffs_list.append(DiffMethod(file_name=blob.path, class_name=c, method_b=m, added=True))
        return diffs_list

    def get_modified_file_diffs(self, blob_a, blob_b):
        diffs_list = [DiffFile(file_a=blob_a.path, file_b=blob_b.path, modified=True)]
        try:
            if can_parse_file(blob_a.path) and can_parse_file(blob_b.path) and self.method_granularity:
                source_a = GitExtractor.get_source(blob_a)
                source_b = GitExtractor.get_source(blob_b)
                diffs_list.extend(GitExtractor.diff((blob_a.path, source_a), (blob_b.path, source_b)))
        except ParsingError:
            pass
        return diffs_list

    def get_renamed_file_diffs(self, blob_a, blob_b):
        diffs_list = [DiffFile(file_a=blob_a.path, file_b=blob_b.path, renamed=True)]
        try:
            if can_parse_file(blob_a.path) and can_parse_file(blob_b.path) and self.method_granularity:
                source_a = GitExtractor.get_source(blob_a)
                source_b = GitExtractor.get_source(blob_b)
                diffs_list.extend(GitExtractor.diff((blob_a.path, source_a), (blob_b.path, source_b)))
        except ParsingError:
            pass
        return diffs_list

    def is_good_blob(self, blob):
        return blob and is_code_file(blob.path) and not re.search(self.ignore_regex, blob.path)

    @staticmethod
    def get_source(blob):
        try:
            stream = blob.data_stream.read()
            source = stream.decode("UTF-8")
        except AttributeError:
            raise ParsingError
        return source

    @staticmethod
    def parse(path, source):
        try:
            if "java" in path:
                components = JavaParser.parse(source)
                return components
        except ParsingError:
            pass
        return False

    @staticmethod
    def diff(file_a, file_b):
        try:
            if "java" in file_a[0]:
                components_diff = JavaParser.diff(file_a, file_b)
                return components_diff
        except ParsingError:
            pass
        return []