from extraction.git_extractor import GitExtractor
from analysis.time_weighted_risk import *

repo = GitExtractor("/Users/andre/git/budibox/.git")
time_weighted_risk(repo)