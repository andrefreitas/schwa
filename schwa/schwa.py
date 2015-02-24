from extraction.git_extractor import GitExtractor
from repository.repository import  Repository
from analysis.time_weighted_risk import TimeWeightedRiskAnalysis


class Schwa:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def analyze(self,  ignore_regex="^$", max_commits=None):
        extractor = GitExtractor(self.repo_path)
        repo = extractor.extract(ignore_regex, max_commits)
        analysis = TimeWeightedRiskAnalysis(repo)
        metrics = analysis.analyze()
        return metrics


