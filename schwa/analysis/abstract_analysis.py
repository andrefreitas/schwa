import abc


class AbstractAnalysis:
    __metaclass__ = abc.ABCMeta

    def __init__(self, repository):
        self.repository = repository

    @abc.abstractmethod
    def analyze(self):
        """ does the analysis of the repository and outputs metrics for each component"""
