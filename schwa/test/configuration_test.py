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

""" Module for testing configurations. """

import unittest

from schwa import Schwa, SchwaConfigurationException
from schwa.analysis import Metrics

class TestFeatureWeightLearner(unittest.TestCase):
    def setUp(self):
        self.r_w = Metrics.REVISIONS_WEIGHT
        self.f_w = Metrics.FIXES_WEIGHT
        self.a_w = Metrics.AUTHORS_WEIGHT

    def reset_weights(self):
        Metrics.REVISIONS_WEIGHT = self.r_w
        Metrics.FIXES_WEIGHT = self.f_w
        Metrics.AUTHORS_WEIGHT = self.a_w

    def test_valid_configuration(self):
        s = Schwa(".")
        configs = {
            "commits": 100,
            "features_weights": {
                "revisions": 0.2,
                "fixes": 0.3,
                "authors": 0.5
            }
        }
        max_commits = None
        max_commits = s.configure_yaml(configs, max_commits)
        self.assertEqual(max_commits, 100)
        self.assertEqual(Metrics.REVISIONS_WEIGHT, 0.2)
        self.assertEqual(Metrics.FIXES_WEIGHT, 0.3)
        self.assertEqual(Metrics.AUTHORS_WEIGHT, 0.5)

        max_commits = 2
        max_commits = s.configure_yaml(configs, max_commits)
        self.assertEqual(max_commits, 2)

        del configs["features_weights"]
        self.reset_weights()
        s.configure_yaml(configs, max_commits)
        self.assertEqual(Metrics.REVISIONS_WEIGHT, self.r_w)
        self.assertEqual(Metrics.FIXES_WEIGHT, self.f_w)
        self.assertEqual(Metrics.AUTHORS_WEIGHT, self.a_w)

    def test_wrong_weights(self):
        s = Schwa(".")
        configs = {
            "commits": 100,
            "features_weights": {
                "revisions": 0.4,
                "fixes": 0.3,
                "authors": 0.5
            }
        }
        self.reset_weights()
        max_commits = None

        with self.assertRaises(SchwaConfigurationException):
            max_commits = s.configure_yaml(configs, max_commits)

    def tearDown(self):
        self.reset_weights()

