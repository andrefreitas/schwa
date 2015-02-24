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
        print("Analyzing " + max_commits + " commits...")
        s = Schwa(repository_path)
        metrics = s.analyze(ignore_regex, max_commits)
        metrics = {k: v for k, v in metrics.items() if v > 0}

        if len(metrics.items()) > 0:
            metric_sum = 0
            for k, v in metrics.items():
                metric_sum = metric_sum + v
            metrics = {k: v/metric_sum for k, v in metrics.items()}
            print("Defect probability based from previous defects:")
            print("")
            for k, v in metrics.items():
                print(k + "  -  " + "{:.00%}".format(v))
        else:
            print("Not enough data to compute metrics...")