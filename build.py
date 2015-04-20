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

""" Script to build binaries. """

from cx_Freeze import setup, Executable
from schwa.schwa import VERSION

include_files = [
    ("schwa/web/views/index.tpl", "views/index.tpl"),
    ("schwa/web/static/app.js", "static/app.js"),
    ("schwa/web/static/d3.min.js", "static/d3.min.js"),
    ("schwa/web/static/styles.css", "static/styles.css"),
]

setup(
    name="schwa",
    version=VERSION,
    description="A tool that predicts Software defects from GIT repositories.",
    executables=[Executable(script="debug.py", targetName="schwa")],
    options=dict(build_exe={"include_files": include_files})
)
