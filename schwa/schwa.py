from extraction.git_extractor import GitExtractor
from repository.repository import  Repository
from analysis.time_weighted_risk import TimeWeightedRiskAnalysis


class Schwa:
    def __init__(self, repo_path, ignore_regex="^$"):
        self.repo_path = repo_path
        self.ignore_regex = ignore_regex

    def analyze(self):
        extractor = GitExtractor(self.repo_path, self.ignore_regex)
        files = extractor.files()
        commits = extractor.commits()
        timestamp = extractor.timestamp()
        repo = Repository(self.repo_path, commits, files, timestamp)
        analysis = TimeWeightedRiskAnalysis(repo)
        metrics = analysis.analyze()
        return metrics


