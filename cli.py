import sys
import os
from schwa.schwa import Schwa

if len(sys.argv) < 4:
    print("usage:", sys.argv[0], "repository_path", "max_commits", "granularity", "[ignore_regex]")
else:
    ignore_regex = "^$"
    max_commits = sys.argv[2]
    repository_path = sys.argv[1]
    method_granularity = sys.argv[3] == "method"

    if len(sys.argv) == 5:
        ignore_regex = sys.argv[4]

    if not os.path.exists(repository_path):
        print("Invalid repository path")
    else:
        print("Analyzing up to " + max_commits + " commits...")
        s = Schwa(repository_path)
        analytics = s.analyze(ignore_regex, max_commits, method_granularity)
        print("Repository Analytics:")
        print("Fixes:", analytics.fixes)
        print("Java Code Revisions:", analytics.revisions)
        print("")



