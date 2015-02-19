from git import *
import re


class GitExtractor:

    def __init__(self, path):
        self.path = path
        self.repo = Repo(path)

    def get_code_files(self):
        tree_traverse = self.repo.head.commit.tree.traverse()
        code_files = [item.path for item in tree_traverse if item.type == 'blob' and is_code_file(item.path)]
        return code_files

    def get_commits(self):
        return list(self.repo.iter_commits())

    def get_commit_files(self, commit):
        changed_files = []
        for parent in commit.parents:
            diffs = commit.diff(parent)
            code_files = [diff.a_blob.path for diff in diffs if is_code_file(diff.a_blob.path)]
            changed_files = changed_files + [f for f in code_files if f not in changed_files]
        return changed_files

    def start_timestamp(self):
        return list(self.repo.iter_commits())[-1].committed_date





def is_code_file(path):
    result = re.search(".+\.(java|php|py|cpp|c|js|html|css|rb)", path)
    return result
