# _Schwa_ [![Build Status](https://magnum.travis-ci.com/andrefreitas/schwa.svg?token=eMdED9z4qEU8n9mx58dz&branch=andre)](https://magnum.travis-ci.com/andrefreitas/schwa)

A tool that analyzes GIT Repositories of Java Projects and estimates the defect probability of Software components.

## Install
1. Install Python 3.4 and pip
2. Install Git
3. Run `python3.4 setup.py install`

## Usage
Command line:

`schwa repository_path [max_commits]`

Importing class:
```python
from schwa import Schwa
s = Schwa(repository_path)
analytics = s.analyze()
```

## Contribute
1. Install Python 3.4 and pip
2. Install Git
3. Run `pip3.4 install -r requirements.txt`
4. Use an IDE such as Pycharm

## Test
Run `nosetests`
