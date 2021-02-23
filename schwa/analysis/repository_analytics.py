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
is computed. Science is being done here! We use Decimal from the standard library
since results were accumulating errors.
"""

import re
from decimal import Decimal


class Metrics:
    """ A class for representing a set of Metrics.

    In analysis, each component have their analytics represented by a Metric instance.

    Attributes:
        fixes_dataset: A set of (revisions_twr, fixes_twr, authors_twr) that had a bug.
        FIXES_WEIGHT: A Decimal having the fixes weight for the defect probability computation.
        AUTHORS_WEIGHT: A Decimal having the authors weight for the defect probability computation.
        REVISIONS_WEIGHT: A Decimal having the revisions weight for the defect probability computation.
        TIME_RANGE: A Decimal from 0 to 1 that changes the time range of the TWR function.
        revisions_timestamps: A list that stores the timestamps of every revision.
        fixes_timestamps: A list that stores the timestamps of every bug fixing.
        authors_timestamps: A list that stores the timestamps of when a component had a new author.
        revisions_twr: A Decimal that is an accumulator of revisions TWR (see TWR formula).
        fixes_twr: A Decimal that is an accumulator of fixes TWR (see TWR formula).
        authors_twr: A Decimal that is an accumulator of authors TWR (see TWR formula).
        authors: A set that have all email of authors that contributed (see TWR formula).
        fixes: An int that is a counter of bug fixes.
        revisions: An int that is a counter of revisions.
        defect_prob: A Decimal representing the defect probability.
    """

    fixes_dataset = set()
    FIXES_WEIGHT = Decimal(0.5)
    AUTHORS_WEIGHT = Decimal(0.25)
    REVISIONS_WEIGHT = Decimal(0.25)
    TIME_RANGE = Decimal(0.4)

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
        self.defect_prob = 0
        self.last_twr = None

    @staticmethod
    def twr(begin_ts, ts, current_ts):
        """ Computes a Time Weighted Risk parcel.

        Normalizes the timestamps and returns the TWR parcel.

        Args:
            begin_ts: An int representing the beginning timestamp.
            ts: An int representing a specific timestamp.
            current_ts: An int representing the most recent timestamp.

        Returns:
            A Decimal from 0 to 0.5.
        """

        begin_diff = ts - begin_ts
        diff = current_ts - begin_ts
        if diff == 0:
            normalized = 1
        else:
            normalized = Decimal(begin_diff) / Decimal(diff)
        twr = 1 / (1 + Decimal.exp(Decimal(-12) * normalized + Decimal(2) + ((1 - Metrics.TIME_RANGE) * 10)))
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
            begin_ts: An int that is timestamp of the first commit.
        """

        if self.revisions_timestamps:
            last_revision_timestamp = self.revisions_timestamps[-1]
            revisions_twr = Metrics.list_twr(self.revisions_timestamps, begin_ts, last_revision_timestamp)
            fixes_twr = Metrics.list_twr(self.fixes_timestamps, begin_ts, last_revision_timestamp)
            authors_twr = Metrics.list_twr(self.authors_timestamps, begin_ts, last_revision_timestamp)
            self.last_twr = (revisions_twr, fixes_twr, authors_twr)
            Metrics.fixes_dataset.add((revisions_twr, fixes_twr, authors_twr))

    def defect_probability(self):
        probability = Metrics.compute_defect_probability(self.revisions_twr, self.fixes_twr, self.authors_twr,
                                                         Metrics.REVISIONS_WEIGHT, Metrics.FIXES_WEIGHT,
                                                         Metrics.AUTHORS_WEIGHT)
        return probability

    @staticmethod
    def compute_defect_probability(r_twr, f_twr, a_twr, r_weight, f_weight, a_weight):
        twr = r_twr * r_weight + f_twr * f_weight + a_twr * a_weight
        probability = 1 - Decimal.exp(- twr)
        return probability

    def to_dict(self):
        metrics_dict = {
            "size": str(self.defect_prob),
            "prob": str(self.defect_prob),
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
        analytics: A dict that maps files paths to FileAnalytics instances.
    """

    def __init__(self):
        super().__init__()
        self.analytics = {}

    def is_empty(self):
        return len(self.analytics) == 0

    def compute_defect_probability(self):
        """ Computes the defect probability for every child """
        self.defect_prob = self.defect_probability()
        for analytics in self.analytics.values():
            analytics.compute_defect_probability()

    def to_dict(self, name="root", type=None):
        """ Converts repository analytics to a dict.

        It traverses child analytics to convert and adds some information useful
        for the Sunburst chart.

        Returns:
            A dict of all the analytics collected from the repository.
        """

        metrics_dict = super().to_dict()
        metrics_dict["name"] = name
        metrics_dict["type"] = type
        metrics_dict["children"] = [metrics.to_dict(name) for name, metrics in self.analytics.items()]

        return metrics_dict


class FileAnalytics(RepositoryAnalytics):
    """ A class to represent File Analytics.

    It may stores child lines and classes.
    """

    def __init__(self):
        super().__init__()

    def to_dict(self, name):
        return super().to_dict(name, "file") # TODO strip_path(path)


class ClassAnalytics(RepositoryAnalytics):
    """ A class to represent Class Analytics.

    It may stores child classes, methods, and lines.
    """

    def __init__(self):
        super().__init__()

    def to_dict(self, name):
        return super().to_dict(name, "class")


class MethodAnalytics(RepositoryAnalytics):
    """ A class to represent Method Analytics.

    It may stores child methods, and lines.
    """

    def __init__(self):
        super().__init__()

    def to_dict(self, name):
        return super().to_dict(name, "method")


class LineAnalytics(RepositoryAnalytics):
    """ A class to represent Line Analytics

    It is the leaf of analytics.
    """
    def __init__(self):
        super().__init__()

    def to_dict(self, name):
        return super().to_dict(name, "line")