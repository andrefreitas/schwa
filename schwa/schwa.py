from extraction.git_extractor import GitExtractor
from repository.repository import  Repository
from analysis.time_weighted_risk import TimeWeightedRiskAnalysis


class Schwa:
    def __init__(self, repo_path, ignore_regex="^$"):
        self.repo_path = repo_path
        self.ignore_regex = ignore_regex

    def analyze(self, commits_number=None):
        extractor = GitExtractor(self.repo_path, self.ignore_regex)
        files = extractor.files()
        commits = extractor.commits_parallels(commits_number)
        #commits = extractor.commits(commits_number)
        timestamp = extractor.timestamp()
        repo = Repository(self.repo_path, commits, files, timestamp)
        analysis = TimeWeightedRiskAnalysis(repo)
        metrics = analysis.analyze()
        return metrics


