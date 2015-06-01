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

""" Command Line Interface Module. """

import os
import argparse
import signal
import sys
from schwa.web import Server
from schwa import Schwa, SchwaConfigurationException
from schwa.extraction import RepositoryExtractionException


def main():
    dir = os.path.dirname(os.path.abspath(__file__))
    version = {}
    with open(os.path.join(dir, "version.py")) as fp:
        exec(fp.read(), version)

    cli = CLI(version['__version__'])
    cli.run()


class CLI:
    """ Class for wrapping the CLI interface.

    Attributes:
        args: command line arguments
        version: schwa version
    """
    def __init__(self, version):
        self.args = None
        self.version = version
        self.config()

    def config(self):
        parser = argparse.ArgumentParser(description='Predicts defects from GIT repositories.')
        parser.add_argument('repository', help="repository full path on local file system")
        parser.add_argument('--commits', help="maximum number of commits, since the last one, to be analyzed",
                            default=None, type=int)
        parser.add_argument('-s', '--single', action='store_true', help="Runs in a single process instead of parallel")
        parser.add_argument('-j', '--json', action='store_true', help="Outputs results as JSON")
        parser.add_argument('-l', '--learn', action='store_true', help="Learn features weight")
        parser.add_argument('--bits', help="Features weight learning bits precision", default=None, type=int)
        parser.add_argument('--generations', help="Features weight learning bits generations", default=None, type=int)
        parser.add_argument('--version', action='version', version='%(prog)s ' + self.version)
        self.args = parser.parse_args()

    def routes(self):
        signal.signal(signal.SIGINT, Controller.exit)

        if not os.path.exists(self.args.repository):
            Controller.invalid_repo(self.args)

        elif self.args.json:
            Controller.run_json(self.args)

        elif self.args.learn:
            Controller.learn(self.args)
        else:
            Controller.run(self.args)

    def check_updates(self):
        #TODO: Write an update checker in a Thread
        url = "https://pypi.python.org/pypi/Schwa/json"
        pass

    def run(self):
        self.routes()


class Controller:
    @staticmethod
    def run(args):
        Views.wait()
        try:
            s = Schwa(args.repository)
            analytics = s.analyze(max_commits=args.commits, parallel=not args.single)
            Views.results(analytics)
        except (RepositoryExtractionException, SchwaConfigurationException) as e:
            Views.failed(e)
            sys.exit(1)

    @staticmethod
    def run_json(args):
        s = Schwa(args.repository)
        analytics = s.analyze(max_commits=args.commits, parallel=not args.single)
        Views.results_json(analytics)

    @staticmethod
    def invalid_repo(args):
        Views.invalid_repo()
        sys.exit(1)

    @staticmethod
    def exit(signum, frame):
        sys.exit(0)

    @staticmethod
    def learn(args):
        Views.wait()
        try:
            s = Schwa(args.repository)
            solution = s.learn(max_commits=args.commits, parallel=not args.single, bits=args.bits,
                               generations=args.generations)
            Views.learn(solution, args.repository, args.commits)
        except (RepositoryExtractionException, SchwaConfigurationException) as e:
            Views.failed(e)
            sys.exit(1)


class Views:
    @staticmethod
    def wait():
        print("Please wait...")

    @staticmethod
    def results(analytics):
        if analytics.is_empty():
            print("Couldn't find enough data to produce results.")
        else:
            print("Press ctrl+c to exit")
            Server.run(analytics)

    @staticmethod
    def results_json(analytics):
        if not analytics.is_empty():
            print(analytics.to_dict())

    @staticmethod
    def failed(msg):
        print("Failed:", msg)

    @staticmethod
    def invalid_repo():
        print("Invalid repository path!")

    @staticmethod
    def learn(solution, repository, commits):
        print_param = lambda k: print(k, " : ", str(round(solution[k], 4)))
        print("===================================")
        print("FEATURES WEIGHTS GA LEARNER")
        print("===================================")
        print_param("revisions")
        print_param("fixes")
        print_param("authors")
        print("-----------------------------------")
        print_param("fitness")
        print("-----------------------------------")
        print("repository", ":", repository)
        print("commits", ":", commits if commits else "all")
        print_param("bits")
        print_param("generations")
        print("-----------------------------------")
