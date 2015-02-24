import sys
import os
from schwa import Schwa


if len(sys.argv) < 3:
    print("usage:", sys.argv[0], "repository_path", "max_commits", "[ignore_regex]")
else:
    ignore_regex = "^$"
    max_commits = sys.argv[2]
    repository_path = sys.argv[1]

    if len(sys.argv) == 4:
        ignore_regex = sys.argv[3]

    if not os.path.exists(repository_path):
        print("Invalid repository path")
    else:
        print("Analyzing up to " + max_commits + " commits...")
        s = Schwa(repository_path)
        metrics = s.analyze(ignore_regex, max_commits)

        if len(metrics) > 0:
            print("Metrics:")
            print("")
            for k, v in metrics.items():
                print(k, v)
        else:
            print("Not enough data to compute metrics...")