# Copyright (c) 2015 Faculty of Engineering of the University of Porto
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

""" Module for declaring classes for the analytics/metrics.

This module is the most important to understand the Schwa API.
Here the analytics structure is declared and the defect probability
is computed. Science is being done here!
"""

import math
import re


class Metrics:
    """ A class for representing a set of Metrics.

    In analysis, each component have their analytics represented by a Metric instance.

    Attributes:
        fixes_dataset: A list of (revisions_twr, fixes_twr, authors_twr) that had a bug.
        fixes_weight: A float having the fixes weight for the defect probability computation.
        authors_weight: A float having the authors weight for the defect probability computation.
        revisions_weight: A float having the revisions weight for the defect probability computation.
        revisions_timestamps: A list that stores the timestamps of every revision.
        fixes_timestamps: A list that stores the timestamps of every bug fixing.
        authors_timestamps: A list that stores the timestamps of when a component had a new author.
        revisions_twr: A float that is an accumulator of revisions TWR (see TWR formula).
        fixes_twr: A float that is an accumulator of fixes TWR (see TWR formula).
        authors_twr: A float that is an accumulator of authors TWR (see TWR formula).
        authors: A set that have all email of authors that contributed (see TWR formula).
        fixes: An int that is a counter of bug fixes.
        revisions: An int that is a counter of revisions.
        defect_prob: A float representing the defect probability that is computed a posteriori.
    """

    fixes_dataset = []
    fixes_weight = 0.5
    authors_weight = 0.25
    revisions_weight = 0.25

    def __init__(self):
        """ Inits all metrics. """

        self.revisions_timestamps = []
        self.fixes_timestamps = []
        self.authors_timestamps = []
        self.revisions_twr = 0
        self.fixes_twr = 0
        self.authors_twr = 0
        self.authors = set()
        self.fixes = 0
        self.revisions = 0
        self.defect_prob = 0

    @staticmethod
    def twr(begin_ts, ts, current_ts):
        """ Computes a Time Weighted Risk parcel.

        Normalizes the timestamps and returns the TWR parcel.

        Args:
            begin_ts: An int representing the beginning timestamp.
            ts: An int representing a specific timestamp.
            current_ts: An int representing the most recent timestamp.

        Returns:
            A float from 0 to 0.5.
        """

        begin_diff = ts - begin_ts
        diff = current_ts - begin_ts
        if diff == 0:
            normalized = 0
        else:
            normalized = begin_diff / diff
        twr = 1 / (1 + math.e ** (-12 * normalized + 12))
        return twr

    @staticmethod
    def list_twr(seq, begin_ts, current_ts):
        """ Computes the TWR sum from a list.

        By receiving a list, computes the TWR sum, by giving the begin timestamp
        and the most current timestamp.

        Args:
            seq: A list of timestamps ints.
            begin_ts: An int representing the beginning timestamp.
            current_ts: An int representing the most recent timestamp.

        Returns:
            A float representing the TWR sum.
        """

        twr_sum = 0
        for ts in seq:
            twr_sum += Metrics.twr(begin_ts, ts, current_ts)
        return twr_sum

    def update(self, begin_ts, ts, current_ts, author, is_bug_fixing):
        """ Updates metrics.

        By receiving the commit information, updates the existing metrics.

        Args:
            begin_ts: An int representing the beginning timestamp.
            ts: An int representing a specific timestamp.
            current_ts: An int representing the most recent timestamp.
            author: A string representing the author email.
            is_bug_fixing: A boolean that indicates if is a bug fixing commit
        """

        # Updates fixes
        if is_bug_fixing:
            self.add_to_dataset(begin_ts)
            self.fixes += 1
            self.fixes_timestamps.append(ts)
            self.fixes_twr += Metrics.twr(begin_ts, ts, current_ts)
        # Updates revisions
        self.revisions += 1
        self.revisions_timestamps.append(ts)
        self.revisions_twr += Metrics.twr(begin_ts, ts, current_ts)
        # Updates authors
        if author not in self.authors:
            self.authors.add(author)
            self.authors_timestamps.append(ts)
            self.authors_twr += Metrics.twr(begin_ts, ts, current_ts)

    def add_to_dataset(self, begin_ts):
        """ Adds a bug case to a dataset.

        Adds (revisions_twr, fixes_twr, authors_twr) when a bug fix happened,
        since this metrics indicate a presence of a bug. The reasoning is that
        in the last revision, the component had a bug.

        Args:
            begin_ts: The timestamp of the first commit.
        """

        if self.revisions_timestamps:
            last_revision_timestamp = self.revisions_timestamps[-1]
            revisions_twr = Metrics.list_twr(self.revisions_timestamps, begin_ts, last_revision_timestamp)
            fixes_twr = Metrics.list_twr(self.fixes_timestamps, begin_ts, last_revision_timestamp)
            authors_twr = Metrics.list_twr(self.authors_timestamps, begin_ts, last_revision_timestamp)
            Metrics.fixes_dataset.append((revisions_twr, fixes_twr, authors_twr))

    def defect_probability(self):
        """ Computes the defect probability. """
        twr = Metrics.fixes_weight * self.fixes_twr + Metrics.revisions_weight * self.revisions_twr \
            + Metrics.authors_weight * self.authors_twr
        probability = 1 - math.e ** (- twr)
        return probability

    def to_dict(self):
        metrics_dict = {
            "size": self.defect_prob,
            "prob": self.defect_prob,
            "revisions": self.revisions,
            "fixes": self.fixes,
            "authors": len(self.authors)
        }
        return metrics_dict


def strip_path(path):
    """ Extracts only the file name of a path """
    name_re = re.compile("[^/]*\.([a-z]+)$")
    return name_re.search(path).group(0)


class RepositoryAnalytics(Metrics):
    """ Represents the Analytics of a Repository.

    It stores the files analytics using a dict.

    Attributes:
        files_analytics: A dict that maps files paths to FileAnalytics instances.

    """

    def __init__(self):
        super().__init__()
        self.files_analytics = {}

    def is_empty(self):
        return len(self.files_analytics) == 0

    def compute_defect_probability(self):
        """ Computes the defect probability for every child """
        self.defect_prob = self.defect_probability()
        for file_analytics in self.files_analytics.values():
            file_analytics.compute_defect_probability()

    def to_dict(self):
        """ Converts repository analytics to a dict.

        It traverses child analytics to convert and adds some information useful
        for the Sunburst chart.

        Returns:
            A dict of all the analytics collected from the repository.
        """

        children = [f_metrics.to_dict(f_path) for f_path, f_metrics in self.files_analytics.items()]
        metrics = {
            "name": "root",
            "children": children
        }
        return metrics


class FileAnalytics(Metrics):
    """ A class to represent File Analytics.

    It stores child classes with a dict.

    Attributes:
        classes_analytics: A dict that maps classes names to ClassAnalytics instances.
    """

    def __init__(self):
        super().__init__()
        self.classes_analytics = {}

    def compute_defect_probability(self):
        self.defect_prob = self.defect_probability()
        for class_analytics in self.classes_analytics.values():
            class_analytics.compute_defect_probability()

    def to_dict(self, path):
        metrics_dict = super().to_dict()
        metrics_dict["type"] = "file"
        metrics_dict["path"] = path
        metrics_dict["name"] = strip_path(path)
        metrics_dict["children"] = [c_metrics.to_dict(c_name) for c_name, c_metrics in self.classes_analytics.items()]
        return metrics_dict


class ClassAnalytics(Metrics):
    """ A class to represent Class Analytics.

    It stores child methods and classes with a dict.

    Attributes:
        methods_analytics: A dict that maps methods names to MethodAnalytics instances.
        classes_analytics: A dict that maps classes names to ClassAnalytics instances.
    """

    def __init__(self):
        super().__init__()
        self.methods_analytics = {}
        self.classes_analytics = {}

    def compute_defect_probability(self):
        self.defect_prob = self.defect_probability()
        for method_analytics in self.methods_analytics.values():
            method_analytics.compute_defect_probability()

    def to_dict(self, name):
        metrics_dict = super().to_dict()
        metrics_dict["type"] = "class"
        metrics_dict["name"] = name
        metrics_dict["children"] = [m_metrics.to_dict(m_name) for m_name, m_metrics in self.methods_analytics.items()]
        metrics_dict["children"].extend([c_metrics.to_dict(c_name) for c_name,
                                                                       c_metrics in self.classes_analytics.items()])
        return metrics_dict


class MethodAnalytics(Metrics):
    """ A class to represent Method Analytics

    It the leaf of analytics.
    """
    def __init__(self):
        super().__init__()

    def compute_defect_probability(self):
        self.defect_prob = self.defect_probability()

    def to_dict(self, name):
        metrics_dict = super().to_dict()
        metrics_dict["type"] = "method"
        metrics_dict["name"] = name
        return metrics_dict
