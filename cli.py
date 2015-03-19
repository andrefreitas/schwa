import sys
import os
from schwa.schwa import Schwa
from schwa.web import Server

if len(sys.argv) < 2:
    print("usage:", sys.argv[0], "repository_path", "[max_commits]")
else:
    max_commits = None
    repository_path = sys.argv[1]
    if len(sys.argv) == 3:
        max_commits = int(sys.argv[2])
    if not os.path.exists(repository_path):
        print("Invalid repository path")
    else:
        print("Analyzing up to " + str(max_commits) + " commits...")
        s = Schwa(repository_path)
        analytics = s.analyze(max_commits=max_commits)
        Server.run(analytics)