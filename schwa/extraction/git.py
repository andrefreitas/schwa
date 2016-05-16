""" Extraction of git repositories history """

import git
import re
from schwa.repository import Commit, Diff, source


EXTENSIONS = [ "java", "php", "py", "cc", "cpp", "c", "go"]

def ignore_blob(blob):
    if blob:
        is_code = re.search(".+\.(" + "|".join(EXTENSIONS) + ")$", blob.path)
        return not is_code
    else:
        return False

def extract_new_file_diffs(blob):
    component = source.File(blob.path)
    return [Diff(component_b=component, added=True)]

def extract_renamed_file_diffs(a_blob, b_blob):
    component_a = source.File(a_blob.path)
    component_b = source.File(b_blob.path)
    return [Diff(component_a=component_a, component_b=component_b, renamed=True)]

def extract_deleted_file_diffs(blob):
    component = source.File(blob.path)
    return [Diff(component_a=component, removed=True)]

def extract_modified_file_diffs(a_blob, b_blob):
    import pdb; pdb.set_trace()
    component_a = source.File(a_blob.path)
    component_b = source.File(b_blob.path)
    return [Diff(component_a=component_a, component_b=component_b, modified=True)]

class Git:
    def __init__(self, repository):
        self.git = git.Repo(repository, odbt=git.GitCmdObjectDB)
        self.repository = repository

    def extract(self, max_commits=None):
        commits_iterator = self.git.iter_commits(max_count=max_commits)
        commits = [self.extract_commit(c) for c in commits_iterator]

    def extract_commit(self, commit_obj):
        diffs = self.extract_commit_diffs(commit_obj)
        commit = Commit(
            identifier=commit_obj.hexsha,
            message=commit_obj.message,
            author=commit_obj.author.email,
            timestamp=commit_obj.committed_date,
            diffs=diffs
        )

    def extract_commit_diffs(self, commit):
        diffs = []
        if not commit.parents:
            for blob in [b for b in commit.tree.traverse() if not ignore_blob(b)]:
                diffs.extend(extract_new_file_diffs(blob))
        else:
            for parent in commit.parents:
                for diff in parent.diff(commit):
                    if diff.new_file and not ignore_blob(diff.b_blob):
                        diffs.extend(extract_new_file_diffs(diff.b_blob))
                    elif diff.renamed and not ignore_blob(diff.a_blob) and not ignore_blob(diff.b_blob):
                        diffs.extend(extract_renamed_file_diffs(diff.a_blob, diff.b_blob))
                    elif diff.deleted_file:
                        diffs.extend(extract_deleted_file_diffs(diff.a_blob))
                    else:
                        diffs.extend(extract_modified_file_diffs(diff.a_blob, diff.b_blob))
        return diffs
