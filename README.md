![Alt text](res/logo.png)

 [![Build Status](https://travis-ci.org/andrefreitas/schwa.svg)](https://travis-ci.org/andrefreitas/schwa) [![Codacy Badge](https://www.codacy.com/project/badge/37a57955ae48429796eafa6ee6af94ef)](https://www.codacy.com/app/pandrefreitas_3191/schwa) [![PyPI version](https://badge.fury.io/py/Schwa.svg)](http://badge.fury.io/py/Schwa) [![Join the chat at https://gitter.im/andrefreitas/schwa](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/andrefreitas/schwa?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) ![License](https://img.shields.io/github/license/mashape/apistatus.svg)

A tool that analyzes GIT Repositories and estimates the defect probability of Software components to help developers
focusing their resources to fix bugs where they really are. We are currently supporting method granularity for Java.

*Schwa is under heavy development as a Master Thesis and is only available as pre-release on the Python Package Index.*


## Install
Install Python3 and pip first and then:

`pip3.4 install schwa --pre`

 or

`python3.4 setup.py install`

## Usage
### Command line:

```shell
usage: schwa [-h] [--commits COMMITS] repository

Predicts defects from GIT repositories.

positional arguments:
  repository         repository full path on local file system

optional arguments:
  -h, --help         show this help message and exit
  --commits COMMITS  maximum number of commits, since the last one, to be
                     analyzed
```

### Importing class:
```python
from schwa import Schwa
s = Schwa("git/repo/path")
analytics = s.analyze()
```

### Configuration file
You can configure Schwa parameters using a YAML file. Just place a .schwa.yml file in the root of the
repository and use this example:

```yaml
commits: 20 # maximum commits
features_weights: # sum must be 1
  revisions: 0.3
  fixes: 0.5
  authors: 0.2
```

## Test
Run `nosetests`

## Contributing
Join the mailing list at https://groups.google.com/forum/#!forum/schwa

### Requirements
1. Install Python 3.4 and pip
2. Install Git
3. Run `pip3.4 install -r requirements.txt`
4. Install Pycharm

### Guidelines
* Write tests first using TDD approach
* Document important modules, functions and classes
* Use [Google Python Style Guide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html) and [PEP8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
* Use Pycharm debugger to kill bugs faster
* Contribute to documentation
* Use good design patterns

### Documentation
Project documentation is available in the [Wiki](https://github.com/andrefreitas/schwa/wiki). Please read it to get familiar with the project.

# License
Copyright (c) 2015 Faculty of Engineering of the University of Porto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
