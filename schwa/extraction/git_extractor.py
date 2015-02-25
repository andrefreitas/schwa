import git
from extraction.abstract_extractor import *
from repository.repository import Repository
from repository.commit import Commit
from repository.file import File
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
        files = self.extract_files(ignore_regex)
        timestamp = self.timestamp()
        repo = Repository(commits, files, timestamp)
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
        commits = {commit._id: commit for commit in commits if commit}
        return commits

    def extract_commit(self, hexsha):
        commit = self.repo.commit(hexsha)
        try:
            _id = hexsha
            message = commit.message
            author = commit.author.email
            timestamp = commit.committed_date
            files_ids = {"added": set(), "modified": set(), "renamed": set()}
            is_good_blob = lambda blob: is_code_file(blob.path) and not re.search(self.ignore_regex, blob.path)
            for parent in commit.parents:
                diffs = parent.diff(commit)
                for diff in diffs:
                    if diff.new_file:
                        files_ids["added"].add(diff.b_blob.path) if is_good_blob(diff.b_blob) else None
                    elif diff.renamed:
                        files_ids["renamed"].add((diff.rename_from, diff.rename_to)) if is_good_blob(diff.b_blob) else None
                    elif not diff.deleted_file:
                        files_ids["modified"].add(diff.a_blob.path) if is_good_blob(diff.a_blob) else None

            return Commit(_id, message, author, timestamp, files_ids) if (len(files_ids["added"]) + len(files_ids["modified"]) + len(files_ids["renamed"])) > 0 else None

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