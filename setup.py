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

""" Installation and deployment script. """

from setuptools import setup
from pip.req import parse_requirements

INSTALL_REQUIREMENTS = [str(ir.req) for ir in parse_requirements("requirements.txt")]

setup(name='Schwa',
      version='0.1-dev',
      description='Git Repositories Mining',
      entry_points={
          "console_scripts": ['schwa = schwa.schwa:main']
      },
      author='Andre Freitas',
      author_email='p.andrefreitas@gmail.com',
      url='https://github.com/andrefreitas/schwa',
      packages=['schwa', 'schwa.analysis', 'schwa.extraction',
                'schwa.parsing', 'schwa.repository', 'schwa.web'],
      install_requires=INSTALL_REQUIREMENTS)
