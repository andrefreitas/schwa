import unittest
import time
import datetime
from schwa.analysis import SchwaAnalysis
from schwa.repository import *


class TestSchwaAnalysis(unittest.TestCase):
    def setUp(self):
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
        diffs.append(DiffMethod(file_name="GUI.java", class_name="GUI", method_a="login", method_b="login",
                                modified=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))


        """ Create repository """
        self.repository = Repository(commits, current_ts)

    def test_revisions_importance(self):
        analysis = SchwaAnalysis(self.repository)
        analytics = analysis.analyze()
        self.assertTrue(analytics.files_analytics["API.java"].defect_prob >
                        analytics.files_analytics["Core.java"].defect_prob)

    def test_fixes_importance(self):
        analysis = SchwaAnalysis(self.repository)
        analytics = analysis.analyze()
        self.assertTrue(analytics.files_analytics["Database.java"].defect_prob >
                        analytics.files_analytics["API.java"].defect_prob)

    def test_authors_importance(self):
        analysis = SchwaAnalysis(self.repository)
        analytics = analysis.analyze()
        self.assertTrue(analytics.files_analytics["GUI.java"].defect_prob >
                        analytics.files_analytics["Database.java"].defect_prob)


