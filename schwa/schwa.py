from schwa.extraction import GitExtractor
from schwa.analysis import SchwaAnalysis


class Schwa:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def analyze(self,  ignore_regex="^$", max_commits=None, method_granularity=False):
        extractor = GitExtractor(self.repo_path)
        repo = extractor.extract(ignore_regex, max_commits, method_granularity)
        analysis = SchwaAnalysis(repo)
        analytics = analysis.analyze()
        return analytics