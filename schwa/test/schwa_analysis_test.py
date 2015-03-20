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

""" Module with the Unit tests for the Schwa Analysis. """

import unittest
import time
import datetime
from schwa.analysis import SchwaAnalysis
from schwa.repository import *


class TestSchwaAnalysis(unittest.TestCase):
    def setUp(self):
        """ Creates a repository for testing. """
        current_ts = time.time()
        commits = []

        """ First Commit """
        _id = "7g37ghegewwuygwe8g"
        message = "First commit"
        author = "petergriffin@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=14).total_seconds()
        diffs = []
        diffs.append(DiffFile(file_b="API.java", added=True))
        diffs.append(DiffClass(file_name="API.java", class_b="API", added=True))
        diffs.append(DiffMethod(file_name="API.java", class_name="API", method_b="login", added=True))
        diffs.append(DiffMethod(file_name="API.java", class_name="API", method_b="register", added=True))
        diffs.append(DiffMethod(file_name="API.java", class_name="API", method_b="getShows", added=True))
        diffs.append(DiffFile(file_b="Core.java", added=True))
        diffs.append(DiffClass(file_name="Core.java", class_b="Core", added=True))
        diffs.append(DiffMethod(file_name="Core.java", class_name="Core", method_b="auth", added=True))
        diffs.append(DiffFile(file_b="Database.java", added=True))
        diffs.append(DiffClass(file_name="Database.java", class_b="Database", added=True))
        diffs.append(DiffMethod(file_name="Database.java", class_name="Database", method_b="query", added=True))
        diffs.append(DiffFile(file_b="GUI.java", added=True))
        diffs.append(DiffClass(file_name="GUI.java", class_b="GUI", added=True))
        diffs.append(DiffMethod(file_name="GUI.java", class_name="GUI", method_b="login", added=True))
        diffs.append(DiffFile(file_b="CLI.java", added=True))
        diffs.append(DiffClass(file_name="CLI.java", class_b="CLI", added=True))
        diffs.append(DiffMethod(file_name="CLI.java", class_name="CLI", method_b="login", added=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Second Commit """
        _id = "j398ygfg98h3"
        message = "Second commit"
        author = "petergriffin@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=12).total_seconds()
        diffs = []
        diffs.append(DiffFile(file_a="API.java", file_b="API.java", modified=True))
        diffs.append(DiffClass(file_name="API.java", class_a="API", class_b="API", modified=True))
        diffs.append(DiffMethod(file_name="API.java", class_name="API", method_a="register", method_b="register",
                                modified=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Third Commit """
        _id = "3433g45g56"
        message = "Third commit"
        author = "petergriffin@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=10).total_seconds()
        diffs = []
        diffs.append(DiffFile(file_a="API.java", file_b="API.java", modified=True))
        diffs.append(DiffClass(file_name="API.java", class_a="API", class_b="API", modified=True))
        diffs.append(DiffMethod(file_name="API.java", class_name="API", method_a="login", method_b="register",
                                modified=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Forth Commit """
        _id = "433343gg"
        message = "Forth commit with a bug fix"
        author = "petergriffin@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=5).total_seconds()
        diffs = []
        diffs.append(DiffFile(file_a="Database.java", file_b="Database.java", modified=True))
        diffs.append(DiffClass(file_name="Database.java", class_a="Database", class_b="Database", modified=True))
        diffs.append(DiffMethod(file_name="Database.java", class_name="Database", method_a="query", method_b="query",
                                modified=True))
        diffs.append(DiffFile(file_a="GUI.java", file_b="GUI.java", modified=True))
        diffs.append(DiffClass(file_name="GUI.java", class_a="GUI", class_b="GUI", modified=True))
        diffs.append(DiffMethod(file_name="GUI.java", class_name="GUI", method_a="login", method_b="login",
                                modified=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Fifth Commit """
        _id = "jf74g87fg87"
        message = "Fifth commit"
        author = "stewie@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=2).total_seconds()
        diffs = []
        diffs.append(DiffFile(file_a="GUI.java", file_b="GUI.java", modified=True))
        diffs.append(DiffClass(file_name="GUI.java", class_a="GUI", class_b="GUI", modified=True))
        diffs.append(DiffClass(file_name="GUI.java", class_b="GUIWindows", added=True))
        diffs.append(DiffMethod(file_name="GUI.java", class_name="GUI", method_a="login", method_b="login",
                                modified=True))
        diffs.append(DiffMethod(file_name="GUI.java", class_name="GUI", method_b="recover",
                                added=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Sixth Commit """
        _id = "sdf355dfd"
        message = "Sixth Commit"
        author = "louis@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=2).total_seconds()
        diffs = []
        diffs.append(DiffFile(file_a="CLI.java", file_b="LinuxCLI.java", renamed=True))
        diffs.append(DiffClass(file_name="LinuxCLI.java", class_a="CLI", class_b="LinuxCLI", renamed=True))
        diffs.append(DiffMethod(file_name="LinuxCLI.java", class_name="LinuxCLI", method_a="login",
                                method_b="LinuxLogin", renamed=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Seventh Commit """
        _id = "sdf4445dfd"
        message = "Seventh Commit"
        author = "louis@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=1).total_seconds()
        diffs = []
        diffs.append(DiffFile(file_a="LinuxCLI.java", removed=True))
        diffs.append(DiffClass(file_name="LinuxCLI.java", class_a="LinuxCLI", removed=True))
        diffs.append(DiffMethod(file_name="LinuxCLI.java", class_name="LinuxCLI", method_a="LinuxLogin",
                                removed=True))

        diffs.append(DiffFile(file_a="GUI.java", file_b="GUI.java", modified=True))
        diffs.append(DiffClass(file_name="GUI.java", class_a="GUIWindows", removed=True))
        diffs.append(DiffMethod(file_name="GUI.java", class_name="GUI", method_a="recover",
                                removed=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))


        """ Create repository """
        self.repository = Repository(commits, current_ts, timestamp)
        self.analysis = SchwaAnalysis(self.repository)

    def test_revisions_importance(self):
        analytics = self.analysis.analyze()
        self.assertTrue(analytics.files_analytics["API.java"].defect_prob >
                        analytics.files_analytics["Core.java"].defect_prob,
                        msg="It should give importance to revisions")

    def test_fixes_importance(self):
        analytics = self.analysis.analyze()
        self.assertTrue(analytics.files_analytics["Database.java"].defect_prob >
                        analytics.files_analytics["API.java"].defect_prob, msg="It should give importance to fixes")

    def test_authors_importance(self):
        analytics = self.analysis.analyze()
        self.assertTrue(analytics.files_analytics["GUI.java"].defect_prob >
                        analytics.files_analytics["Database.java"].defect_prob,
                        msg="It should give importance to authors")

    def test_granularity_analysis(self):
        """ Whitebox testing for  granularity analysis. """

        # File Granularity
        repository = Repository(self.repository.commits[-3:], self.repository.begin_ts,
                                self.repository.commits[-1].timestamp)
        analysis = SchwaAnalysis(repository)
        analytics = analysis.analyze()
        self.assertTrue("GUI.java" in analytics.files_analytics, msg="It should deal with non added files")

        repository = Repository(self.repository.commits[:-1], self.repository.begin_ts,
                                self.repository.commits[:-1][-1].timestamp) # Except last commit
        analysis = SchwaAnalysis(repository)
        analytics = analysis.analyze()
        self.assertTrue("LinuxCLI.java" in analytics.files_analytics, msg="It should deal with renamed files")
        self.assertEqual(analytics.files_analytics["LinuxCLI.java"].revisions, 2,
                         msg="It should deal with renamed files")

        analytics = self.analysis.analyze()
        self.assertTrue("LinuxCLI.java" not in analytics.files_analytics, msg="It should deal with removed files")

        self.assertEqual(len(analytics.files_analytics["GUI.java"].authors), 3)
        self.assertEqual(analytics.files_analytics["GUI.java"].fixes, 1)
        self.assertEqual(analytics.files_analytics["GUI.java"].revisions, 4)

        # Class granularity
        self.assertTrue("GUIWindows" not in analytics.files_analytics["GUI.java"].classes_analytics,
                        msg="It should recognize removed classes")

        # Method granularity
        self.assertTrue("recover" not in analytics.files_analytics["GUI.java"].classes_analytics["GUI"].methods_analytics,
                        msg="It should recognize removed methods")


