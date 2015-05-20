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

""" Module for the Feature Weight Learner """

import unittest
import time
import datetime
from schwa.learning import FeatureWeightLearner
from schwa.repository import Repository, DiffMethod, DiffFile, DiffClass, Commit


class TestFeatureWeightLearner(unittest.TestCase):
    def setUp(self):
        commits = []

        current_ts = time.time()

        _id = "7g37ghegewwuygwe8g"
        message = "First commit"
        author = "petergriffin@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=14).total_seconds()
        diffs = []
        diffs.append(DiffFile(file_b="API.java", added=True))
        diffs.append(DiffFile(file_b="Core.java", added=True))
        diffs.append(DiffFile(file_b="Database.java", added=True))
        diffs.append(DiffFile(file_b="GUI.java", added=True))
        diffs.append(DiffFile(file_b="CLI.java", added=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Second Commit """
        _id = "j398ygfg98h3"
        message = "Fixed register method"
        author = "petergriffin@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=2).total_seconds()
        diffs = []
        diffs.append(DiffFile(file_a="API.java", file_b="API.java", modified=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Third Commit """
        _id = "3433g45g56"
        message = "Fixed register method again"
        author = "petergriffin@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=1).total_seconds()
        diffs = []
        diffs.append(DiffFile(file_a="API.java", file_b="API.java", modified=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        self.repository = Repository(commits, current_ts, timestamp)

    def test_revisions_weight(self):
        """ API.Java is the file with most revisions and fixes in the bug introducing change.
        """
        solution = FeatureWeightLearner(self.repository, generations=70).learn()
        self.assertGreater(solution["revisions"], solution["fixes"])
