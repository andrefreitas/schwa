from extraction.git_extractor import *
import re
import time
import math

current_ts = time.time()


def is_bug_fixing(message):
    return re.search("bug|fix", message, re.I)


def normalized_timestamp(begin_ts, ts, current_ts):
    begin_diff = ts - begin_ts
    diff = current_ts - begin_ts
    normalized = begin_diff / diff
    return normalized


def time_weighted_risk(repo):
    rank = {file: 0 for file in repo.get_code_files()}
    bug_fixing_commits = [commit for commit in repo.get_commits() if is_bug_fixing(commit.message)]
    start_ts = repo.start_timestamp()

    for commit in bug_fixing_commits:
        code_changed_files = repo.get_commit_files(commit)
        ts = commit.committed_date
        normalized_ts = normalized_timestamp(start_ts, ts, current_ts)
        calc = 1 / (1 + math.e**(-12 * normalized_ts + 12))

        for f in code_changed_files:
            rank[f] = rank[f] + calc

    return rank



