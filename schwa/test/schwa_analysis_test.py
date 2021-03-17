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

        api_file      = File(path="API.java")
        api_class     = Class("API", 1, 1, api_file)
        api_method_a  = Method("login", 1, 1, api_class)
        api_method_b  = Method("register", 1, 1, api_class)
        api_method_c  = Method("getShows", 1, 1, api_class)
        core_file     = File(path="Core.java")
        core_class    = Class("Core", 1, 1, core_file)
        core_method   = Method("auth", 1, 1, core_class)
        database_file   = File(path="Database.java")
        database_class  = Class("Database", 1, 1, database_file)
        database_method = Method("query", 1, 1, database_class)
        gui_file      = File(path="GUI.java")
        gui_class     = Class("GUI", 1, 1, gui_file)
        gui_method    = Method("login", 1, 1, gui_class)
        cli_file      = File(path="CLI.java")
        cli_class     = Class("CLI", 1, 1, cli_file)
        cli_method    = Method("login", 1, 1, cli_class)

        diffs.append(DiffFile(file_b=api_file, added=True))
        diffs.append(DiffClass(parent=api_file, class_b=api_class, added=True))
        diffs.append(DiffMethod(parent=api_class, method_b=api_method_a, added=True))
        diffs.append(DiffMethod(parent=api_class, method_b=api_method_b, added=True))
        diffs.append(DiffMethod(parent=api_class, method_b=api_method_c, added=True))
        diffs.append(DiffFile(file_b=core_file, added=True))
        diffs.append(DiffClass(parent=core_file, class_b=core_class, added=True))
        diffs.append(DiffMethod(parent=core_class, method_b=core_method, added=True))
        diffs.append(DiffFile(file_b=database_file, added=True))
        diffs.append(DiffClass(parent=database_file, class_b=database_class, added=True))
        diffs.append(DiffMethod(parent=database_class, method_b=database_method, added=True))
        diffs.append(DiffFile(file_b=gui_file, added=True))
        diffs.append(DiffClass(parent=gui_file, class_b=gui_class, added=True))
        diffs.append(DiffMethod(parent=gui_class, method_b=gui_method, added=True))
        diffs.append(DiffFile(file_b=cli_file, added=True))
        diffs.append(DiffClass(parent=cli_file, class_b=cli_class, added=True))
        diffs.append(DiffMethod(parent=cli_class, method_b=cli_method, added=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Second Commit """
        _id = "j398ygfg98h3"
        message = "Second commit"
        author = "petergriffin@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=12).total_seconds()
        diffs = []
        api_file      = File(path="API.java")
        api_class     = Class("API", 1, 1, api_file)
        api_method    = Method("register", 1, 1, api_class)
        diffs.append(DiffFile(file_a=api_file, file_b=api_file, modified=True))
        diffs.append(DiffClass(parent=api_file, class_a=api_class, class_b=api_class, modified=True))
        diffs.append(DiffMethod(parent=api_class, method_a=api_method, method_b=api_method, modified=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Third Commit """
        _id = "3433g45g56"
        message = "Third commit"
        author = "petergriffin@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=10).total_seconds()
        diffs = []
        api_file      = File(path="API.java")
        api_class     = Class("API", 1, 1, api_file)
        api_method_a  = Method("login", 1, 1, api_class)
        api_method_b  = Method("register", 1, 1, api_class)
        diffs.append(DiffFile(file_a=api_file, file_b=api_file, modified=True))
        diffs.append(DiffClass(parent=api_file, class_a=api_class, class_b=api_class, modified=True))
        diffs.append(DiffMethod(parent=api_class, method_a=api_method_a, method_b=api_method_b, modified=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Forth Commit """
        _id = "433343gg"
        message = "Forth commit with a bug fix"
        author = "petergriffin@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=5).total_seconds()
        diffs = []
        database_file   = File(path="Database.java")
        database_class  = Class("Database", 1, 1, database_file)
        database_method = Method("query", 1, 1, database_class)
        diffs.append(DiffFile(file_a=database_file, file_b=database_file, modified=True))
        diffs.append(DiffClass(parent=database_file, class_a=database_class, class_b=database_class, modified=True))
        diffs.append(DiffMethod(parent=database_class, method_a=database_method, method_b=database_method, modified=True))
        gui_file      = File(path="GUI.java")
        gui_class     = Class("GUI", 1, 1, gui_file)
        gui_method    = Method("login", 1, 1, gui_class)
        diffs.append(DiffFile(file_a=gui_file, file_b=gui_file, modified=True))
        diffs.append(DiffClass(parent=gui_file, class_a=gui_class, class_b=gui_class, modified=True))
        diffs.append(DiffMethod(parent=gui_class, method_a=gui_method, method_b=gui_method, modified=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Fifth Commit """
        _id = "jf74g87fg87"
        message = "Fifth commit"
        author = "stewie@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=2).total_seconds()
        diffs = []
        gui_file      = File(path="GUI.java")
        gui_class     = Class("GUI", 1, 1, gui_file)
        gui_method_a  = Method("login", 1, 1, gui_class)
        gui_method_b  = Method("recover", 1, 1, gui_class)
        diffs.append(DiffFile(file_a=gui_file, file_b=gui_file, modified=True))
        diffs.append(DiffClass(parent=gui_file, class_a=gui_class, class_b=gui_class, modified=True))
        diffs.append(DiffClass(parent=gui_file, class_b=Class("GUIWindows", 1, 1, gui_file), added=True))
        diffs.append(DiffMethod(parent=gui_class, method_a=gui_method_a, method_b=gui_method_a, modified=True))
        diffs.append(DiffMethod(parent=gui_class, method_b=gui_method_b, added=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Sixth Commit """
        _id = "sdf355dfd"
        message = "Sixth Commit"
        author = "louis@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=2).total_seconds()
        diffs = []
        cli_file       = File(path="CLI.java")
        # cli_class      = Class("CLI", 1, 1, cli_file)
        # cli_method     = Method("login", 1, 1, cli_file)
        linux_cli_file   = File(path="LinuxCLI.java")
        # linux_cli_class  = Class("LinuxCLI", 1, 1, linux_cli_file)
        # linux_cli_method = Method("LinuxLogin", 1, 1, linux_cli_file)
        diffs.append(DiffFile(file_a=cli_file, file_b=linux_cli_file, renamed=True))
        # diffs.append(DiffClass(parent=cli_file, class_a=cli_class, class_b=linux_cli_class, renamed=True))
        # diffs.append(DiffMethod(parent=cli_class, method_a=cli_method, method_b=linux_cli_method, renamed=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Seventh Commit """
        _id = "sdf4445dfd"
        message = "Seventh Commit"
        author = "louis@familyguy.com"
        timestamp = current_ts - datetime.timedelta(days=1).total_seconds()
        diffs = []

        linux_cli_file   = File(path="LinuxCLI.java")
        # linux_cli_class  = Class("LinuxCLI", 1, 1, linux_cli_file)
        # linux_cli_method = Method("LinuxLogin", 1, 1, linux_cli_file)
        diffs.append(DiffFile(file_a=linux_cli_file, removed=True))
        # diffs.append(DiffClass(parent=linux_cli_file, class_a=linux_cli_class, removed=True))
        # diffs.append(DiffMethod(parent=linux_cli_class, method_a=linux_cli_method, removed=True))

        gui_file      = File(path="GUI.java")
        gui_class     = Class("GUI", 1, 1, gui_file)
        gui_method    = Method("recover", 1, 1, gui_class)
        diffs.append(DiffFile(file_a=gui_file, file_b=gui_file, modified=True))
        diffs.append(DiffClass(parent=gui_file, class_a=Class("GUIWindows", 1, 1, gui_file), removed=True))
        diffs.append(DiffMethod(parent=gui_class, method_a=gui_method, removed=True))
        commits.append(Commit(_id, message, author, timestamp, diffs))

        """ Create repository """
        self.repository = Repository(commits, current_ts, timestamp)
        self.analysis = SchwaAnalysis(self.repository)

    def test_revisions_importance(self):
        analytics = self.analysis.analyze().analytics

        api_java  = None
        core_java = None
        for analytic in analytics:
            if analytic.name == "API.java":
                api_java = analytic
            if analytic.name == "Core.java":
                core_java = analytic
        self.assertTrue(api_java != None)
        self.assertTrue(core_java != None)

        self.assertTrue(api_java.defect_prob > core_java.defect_prob, msg="It should give importance to revisions")

    def test_fixes_importance(self):
        analytics = self.analysis.analyze().analytics

        database_java  = None
        api_java = None
        for analytic in analytics:
            if analytic.name == "Database.java":
                database_java = analytic
            if analytic.name == "API.java":
                api_java = analytic
        self.assertTrue(database_java != None)
        self.assertTrue(api_java != None)

        self.assertTrue(database_java.defect_prob > api_java.defect_prob, msg="It should give importance to fixes")

    def test_authors_importance(self):
        analytics = self.analysis.analyze().analytics

        database_java  = None
        gui_java = None
        for analytic in analytics:
            if analytic.name == "Database.java":
                database_java = analytic
            if analytic.name == "GUI.java":
                gui_java = analytic
        self.assertTrue(database_java != None)
        self.assertTrue(gui_java != None)

        self.assertTrue(gui_java.defect_prob > database_java.defect_prob, msg="It should give importance to authors")

    def test_granularity_analysis(self):
        """ Whitebox testing for  granularity analysis. """

        # File Granularity
        repository = Repository(self.repository.commits[-3:], self.repository.begin_ts,
                                self.repository.commits[-1].timestamp)
        analysis = SchwaAnalysis(repository)
        analytics = analysis.analyze().analytics
        gui_java = None
        for analytic in analytics:
            if analytic.name == "GUI.java":
                gui_java = analytic
                break
        self.assertTrue(gui_java != None, msg="It should deal with non added files")

        repository = Repository(self.repository.commits[:-1], self.repository.begin_ts,
                                self.repository.commits[:-1][-1].timestamp) # Except last commit
        analysis = SchwaAnalysis(repository)
        analytics = analysis.analyze().analytics
        linux_cli_java = None
        for analytic in analytics:
            if analytic.name == "LinuxCLI.java":
                linux_cli_java = analytic
                break
        self.assertTrue(linux_cli_java != None, msg="It should deal with renamed files")
        self.assertEqual(2, linux_cli_java.revisions, msg="It should deal with renamed files")

        analytics = self.analysis.analyze().analytics
        linux_cli_java = None
        for analytic in analytics:
            if analytic.name == "LinuxCLI.java":
                linux_cli_java = analytic
                break
        self.assertTrue(linux_cli_java == None, msg="It should deal with removed files")

        gui_java = None
        for analytic in analytics:
            if analytic.name == "GUI.java":
                gui_java = analytic
                break
        self.assertTrue(gui_java != None)
        self.assertTrue(3, len(gui_java.authors))
        self.assertTrue(1, gui_java.fixes)
        self.assertTrue(4, gui_java.revisions)

        # Class granularity
        gui_windows_java = None
        for analytic in analytics:
            if analytic.name == "GUIWindows.java":
                for a in analytic.analytics:
                    if a.name == "GUIWindows":
                        gui_windows_java = a
        self.assertTrue(gui_windows_java == None, msg="It should recognize removed classes")

        # Method granularity
        gui_method = None
        for a in gui_java.analytics:
            if a.name == "GUI":
                for b in a.analytics:
                    if b.name == "recover":
                        gui_method = b
        self.assertTrue(gui_method == None, msg="It should recognize removed methods")
