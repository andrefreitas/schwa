import math
from sklearn import svm

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class Metrics:

    dataset = [[], []]
    svm_classifier = svm.SVC(probability=True)

    def __init__(self):
        self.revisions_timestamps = []
        self.fixes_timestamps = []
        self.authors_timestamps = []
        self.revisions_twr = 0
        self.fixes_twr = 0
        self.authors_twr = 0
        self.authors = set()
        self.fixes = 0
        self.revisions = 0

    @staticmethod
    def normalise_timestamp(begin_ts, ts, current_ts):
        begin_diff = ts - begin_ts
        diff = current_ts - begin_ts
        normalized = begin_diff / diff
        return normalized

    @staticmethod
    def twr(begin_ts, ts, current_ts):
        ts = Metrics.normalise_timestamp(begin_ts, ts, current_ts)
        twr = 1 / (1 + math.e ** (-12 * ts + 12))
        return twr

    @staticmethod
    def list_twr(seq, repo_ts, current_ts):
        twr_sum = 0
        for ts in seq:
            twr_sum += Metrics.twr(repo_ts, ts, current_ts)
        return twr_sum

    def update_revisions(self, begin_ts, ts, current_ts):
        self.revisions += 1
        self.revisions_timestamps.append(ts)
        self.revisions_twr += Metrics.twr(begin_ts, ts, current_ts)

    def update_fixes(self, begin_ts, ts, current_ts):
        self.fixes += 1
        self.fixes_timestamps.append(ts)
        self.fixes_twr += Metrics.twr(begin_ts, ts, current_ts)

    def update_authors(self, begin_ts, ts, current_ts, author):
        if author not in self.authors:
            self.authors.add(author)
            self.authors_timestamps.append(ts)
            self.authors_twr += Metrics.twr(begin_ts, ts, current_ts)

    def add_to_dataset(self, repo_ts, current_ts, is_bug_fixing):
        revisions_twr = Metrics.list_twr(self.revisions_timestamps, repo_ts, current_ts)
        fixes_twr = Metrics.list_twr(self.fixes_timestamps, repo_ts, current_ts)
        authors_twr = Metrics.list_twr(self.revisions_timestamps, repo_ts, current_ts)
        label = 1 if is_bug_fixing else 0
        Metrics.dataset[0].append([revisions_twr, fixes_twr, authors_twr])
        Metrics.dataset[1].append(label)

    @staticmethod
    def fit_data():
        Metrics.svm_classifier.fit(Metrics.dataset[0], Metrics.dataset[1])

    def defect_probability(self):
        prob = Metrics.svm_classifier.predict_proba([[self.revisions_twr, self.fixes_twr, self.authors_twr]])
        return prob

    @staticmethod
    def defect_probability(revisions_twr, fixes_twr, authors_twr):
        prob = Metrics.svm_classifier.predict_proba([[revisions_twr, fixes_twr, authors_twr]])
        return prob

    @staticmethod
    def plot(analytics):

        # 3 Features
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for point, bug in zip(Metrics.dataset[0], Metrics.dataset[1]):
            revisions_twr = point[0]
            fixes_twr = point[1]
            authors_twr = point[2]

            if bug == 1:
                ax.scatter(revisions_twr, fixes_twr, 0 ,c='r', marker='o')
            else:
                ax.scatter(revisions_twr, fixes_twr, 0, c='g', marker='o')
        ax.set_xlabel('Revisions')
        ax.set_ylabel('Fixes')
        ax.set_zlabel('Authors')
        plt.show()

        """
        # Revisions Features
        x = []
        y = []
        for file_analytics in analytics.files_analytics.values():
            x.append(file_analytics.revisions_twr)
            y.append(file_analytics.fixes_twr)

        plt.plot(x, y, 'ro')
        plt.xlabel('Revisions TWR')
        plt.ylabel('Fixes TWR')
        plt.axis([0, max(x) + 1, 0, max(y) + 1])
        plt.show()

        # Authors Features
        x = []
        y = []
        for file_analytics in analytics.files_analytics.values():
            x.append(file_analytics.authors_twr)
            y.append(file_analytics.fixes_twr)

        plt.plot(x, y, 'ro')
        plt.xlabel('Authors TWR')
        plt.ylabel('Fixes TWR')
        plt.axis([0, max(x) + 1, 0, max(y) + 1])
        plt.show()



class RepositoryAnalytics(Metrics):
    def __init__(self):
        super().__init__()
        self.files_analytics = {}


class FileAnalytics(Metrics):
    def __init__(self):
        super().__init__()
        self.classes_analytics = {}


class ClassAnalytics(Metrics):
    def __init__(self):
        super().__init__()
        self.methods_analytics = {}


class MethodAnalytics(Metrics):
    def __init__(self):
        super().__init__()