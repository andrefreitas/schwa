from schwa.extraction import GitExtractor
from schwa.analysis import SchwaAnalysis
from schwa.web import Server
import sys
import os


class Schwa:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def analyze(self,  ignore_regex="^$", max_commits=None, method_granularity=True):
        extractor = GitExtractor(self.repo_path)
        repo = extractor.extract(ignore_regex, max_commits, method_granularity)
        analysis = SchwaAnalysis(repo)
        analytics = analysis.analyze()
        return analytics


def main():
    print("Schwa experimental version!!!")
    if len(sys.argv) < 2:
        print("usage:", "schwa", "repository_path", "[max_commits]")
    else:
        max_commits = None
        repository_path = sys.argv[1]
        if len(sys.argv) == 3:
            max_commits = int(sys.argv[2])
        if not os.path.exists(repository_path):
            print("Invalid repository path")
        else:
            print("Analyzing commits...")
            s = Schwa(repository_path)
            analytics = s.analyze(max_commits=max_commits)
            Server.run(analytics)