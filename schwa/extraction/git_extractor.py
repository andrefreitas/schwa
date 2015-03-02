# TODO: Document code

import git
from extraction.abstract_extractor import *
from repository.repository import Repository
from repository.commit import Commit
from repository.file import File
from parsing.java_parser import JavaParser
import multiprocessing

current_repo = None


""" Multiprocessing wrapper """
def extract_commit_wrapper(hexsha):
    return current_repo.extract_commit(hexsha)

""" Multiprocessing wrapper """
def extract_file_wrapper(path):
    return current_repo.extract_file(path)


class GitExtractor(AbstractExtractor):

    def __init__(self, path):
        super().__init__(path)
        self.repo = git.Repo(path, odbt=git.GitCmdObjectDB)

    def extract(self, ignore_regex="^$", max_commits=None):
        global current_repo
        current_repo = self
        commits = self.extract_commits(ignore_regex=ignore_regex, max_commits=max_commits)
        timestamp = self.timestamp()
        repo = Repository(commits, timestamp)
        return repo

    def extract_commits(self, ignore_regex="^$", max_commits=None):
        try:
            cpus = multiprocessing.cpu_count()
        except NotImplementedError:
            cpus = 2   # arbitrary default
        self.ignore_regex = ignore_regex

        iter_commits = self.repo.iter_commits(max_count=max_commits) if max_commits else self.repo.iter_commits()
        commits = [commit.hexsha for commit in iter_commits]
        pool = multiprocessing.Pool(processes=cpus)
        commits = pool.map(extract_commit_wrapper, commits)
        commits = list(reversed([commit for commit in commits if commit]))
        return commits

    def extract_commit(self, hexsha):
        commit = self.repo.commit(hexsha)
        try:
            _id = hexsha
            message = commit.message
            author = commit.author.email
            timestamp = commit.committed_date
            components = {"added": {}, "modified": {}, "renamed": set(), "deleted": {}}
            is_good_blob = lambda blob: blob and is_code_file(blob.path) and not re.search(self.ignore_regex, blob.path)
            for parent in commit.parents:
                diffs = parent.diff(commit)
                for diff in diffs:
                    if not is_good_blob(diff.a_blob) and not is_good_blob(diff.b_blob):
                        continue
                    if diff.new_file:
                        _file = diff.b_blob.path
                        source = diff.b_blob.data_stream.read()
                        classes = GitExtractor.parse_components(_file, source)
                        components["added"][_file] = classes
                    elif diff.renamed:
                        """ A PARTIR DAQUI """
                        if is_good_blob(diff.b_blob):
                            renamed_pair = (diff.rename_from, diff.rename_to)
                            components["renamed"].add(renamed_pair)
                            source_a = diff.a_blob.data_stream.read()
                            source_b = diff.b_blob.data_stream.read()
                            components = GitExtractor.parse_components_diff((diff.a_blob.path, source_a), (diff.b_blob.path, source_b))
                    elif diff.deleted_file:
                        components["deleted"][diff.a_blob.path] = {}
                    else:
                        source_a = diff.a_blob.data_stream.read()
                        source_b = diff.b_blob.data_stream.read()
                        components = GitExtractor.parse_components_diff((diff.a_blob.path, source_a), (diff.b_blob.path, source_b))

            return Commit(_id, message, author, timestamp, components) if (len(components["added"]) + len(components["modified"]) + len(components["renamed"]) + len(components["deleted"])) > 0 else None

        except TypeError:
            return None

    def extract_files(self, ignore_regex):
        tree_traverse = self.repo.head.commit.tree.traverse()
        filter_files = lambda item: item.type == 'blob' \
            and is_code_file(item.path) \
            and not re.search(ignore_regex, item.path)
        code_files = {item.path: File(item.path) for item in tree_traverse if filter_files(item)}
        return code_files

    def timestamp(self):
        return list(self.repo.iter_commits())[-1].committed_date

    @staticmethod
    def parse_components(path, source):
        if "java" in path:
            components = JavaParser.parse(source)
            return components

    @staticmethod
    def parse_components_diff(file_a, file_b):
        if "java" in file_a[0]:
            components_diff = JavaParser.diff(file_a[1], file_b[1])
            return components_diff
