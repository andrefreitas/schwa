# Schwa

[![Build Status](https://travis-ci.org/andrefreitas/schwa.svg)](https://travis-ci.org/andrefreitas/schwa) 

Schwa helps finding code defects by analysing the commits of a repository. You
can use it to help you find the cause of bugs in large projects.

## Install
Make sure you have Python 3 and install with:

    pip install schwa --pre

## Usage
Issue the command in a git repository:

    schwa git/example-repository

Schwa will launch the browser with the results. It's a sunburst that you can
explore. For Java repositories you can explore Classes and Methods.

![Sunburst Chart](schwa/web/static/example.png)
