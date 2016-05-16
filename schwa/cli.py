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

import argparse
import os

from schwa.version import __version__
from schwa.schwa import analyze


def arg_repository(value):
    if not os.path.exists(os.path.join(value, ".git")):
        raise argparse.ArgumentTypeError("%s is an invalid repository path" % value)
    return value

def parse():
    parser = argparse.ArgumentParser(description='Finds defects in source code by mining software history.')
    parser.add_argument('repository', help="repository path", type=arg_repository)
    parser.add_argument('-c', '--commits', help="maximum number of commits", default=None, type=int)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__, help=argparse.SUPPRESS)
    return parser.parse_args()

def main():
    args = parse()
    analyze(args.repository, args.commits)
