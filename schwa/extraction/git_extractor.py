import git
from extraction.abstract_extractor import *
from repository.file import File
from repository.commit import Commit
import multiprocessing


current_repo = None

# Multiprocessing only accepts functions outside classes
def extract_commit_wrapper(hexsha):
    return current_repo.extract_commit(hexsha)


class GitExtractor(AbstractExtractor):

    def __init__(self, path, ignore_regex="^$"):
        super().__init__(path, ignore_regex)
        self.repo = git.Repo(path)

    def files(self):
        tree_traverse = self.repo.head.commit.tree.traverse()
        filter_files = lambda item: item.type == 'blob' \
            and is_code_file(item.path) \
            and not re.search(self.ignore_regex, item.path)
        code_files = [File(item.path) for item in tree_traverse if filter_files(item)]
        return code_files

    def commits_parallels(self, number=None):
        global current_repo
        current_repo = self
        try:
            cpus = multiprocessing.cpu_count()
        except NotImplementedError:
            cpus = 2   # arbitrary default

        commits = [c.hexsha for c in self.repo.iter_commits(max_count=number)] \
            if number else [c.hexsha for c in self.repo.iter_commits()]
        pool = multiprocessing.Pool(processes=cpus)
        commits = pool.map(extract_commit_wrapper, commits)
        commits = [c for c in commits if c]
        return commits

    def extract_commit(self, hexsha):
        commit = self.repo.commit(hexsha)
        try:
            message = commit.message
            author = commit.author.email
            timestamp = commit.committed_date
        except TypeError:
            return None
        files = []
        # Get changes files in commit
        for parent in commit.parents:
            diffs = commit.diff(parent)
            for diff in diffs:
                is_good_blob = lambda blob: blob is not None \
                    and is_code_file(blob.path)\
                    and not re.search(self.ignore_regex, blob.path) \
                    and not blob.path in files
                add_blob = lambda blob: files.append(blob.path) if is_good_blob(blob) else None
                add_blob(diff.a_blob)
                add_blob(diff.b_blob)

        # If files changed are interesting
        if len(files) > 0:
            c = Commit(message, author, timestamp, files)
            return c
        else:
            return None

    def commits(self, number=None):
        commits = []
        iter_commits = self.repo.iter_commits(max_count=number) if number else self.repo.iter_commits()
        for commit in iter_commits:
            try:
                message = commit.message
                author = commit.author.email
                timestamp = commit.committed_date
            except TypeError:
                continue
            files = []
            # Get changes files in commit
            for parent in commit.parents:
                diffs = commit.diff(parent)
                for diff in diffs:
                    is_good_blob = lambda blob: blob is not None \
                        and is_code_file(blob.path)\
                        and not re.search(self.ignore_regex, blob.path) \
                        and not blob.path in files
                    add_blob = lambda blob: files.append(blob.path) if is_good_blob(blob) else None
                    add_blob(diff.a_blob)
                    add_blob(diff.b_blob)

            # If files changed are interesting
            if len(files) > 0:
                c = Commit(message, author, timestamp, files)
                commits.append(c)
        return commits

    def timestamp(self):
        return list(self.repo.iter_commits())[-1].committed_date