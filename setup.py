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


from setuptools import setup, find_packages
import os

dir = os.path.dirname(os.path.abspath(__file__))
version = {}
with open(os.path.join(dir, "schwa", "version.py")) as fp:
    exec(fp.read(), version)

requirements = ["GitPython==0.3.6", "nose==1.3.4", "bottle==0.12.7", "ply==3.4"]
packages = find_packages('.')

setup(name='Schwa',
      version=version["__version__"],
      description='A tool that predicts Software defects from GIT repositories.',
      entry_points={
          "console_scripts": ['schwa = schwa.schwa:main']
      },
      author='Andre Freitas',
      author_email='p.andrefreitas@gmail.com',
      url='https://github.com/andrefreitas/schwa',
      packages=packages,
      package_data={'schwa': ['web/static/*.js', 'web/static/*.css', 'web/views/*.tpl']},
      install_requires=requirements,
      keywords=['testing', 'bugs', 'software'],
      classifiers=[])
