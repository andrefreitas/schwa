# Architecture report
## 1. Glossary
Term  | Description
------------- | -------------
Sunburst Chart | It is a circular statistical graphic, which is divided into slices to illustrate numerical proportion


## 2. Introduction
In this document the main architecture decisions are discussed, by showing class diagrams and explaining the key design decisions.

## 3. Technologies
Schwa is developed in Python, because is a modern, concise language that is easy to learn. It improves software development speed due its simplicity, variety of libraries, good community and easiness of dependency management. We use GitPython that is a pure Python library to interact with GIT repositories. Bottle is used to develop the web server, used to display the Sunburst Chart.

Travis CI is used for continuous integration, to ensure that in every commit the tests are run. Jetbrains Pycharm is the IDE chosen, since it haves a lot of useful feature such as refactoring, debugging, coverage, etc. There is a free Community Edition and a paid Professional Edition, that is actually free for students.

## 4. Logical Architecture
### 4.1 Packages
To improve modularity, Schwa is divided in five main packages.
- **Parsing**: components to parse programming languages;
- **Extraction**: components to interact with software repositories;
- **Repository**: components to model repositories to ensure the domain model is independent of being GIT, SVN, etc;
- **Analysis**: components that analyze a repository and produce metrics, analytics, insights, etc;
- **Web**: components to create a web interface.

## 5. Physical Architecture
Schwa is installed in a local machine as a command line utility and a Python Library.

## 6. Key design decisions
Schwa main module is a facade that receives optional parameters. This helps developers to just know how to call Schwa and do not care about their implementation.

Another important key decision was, in every package, creating abstract classes using template design pattern, to make sure that if, for an instance, we implement a SVN Extractor, it is called the same way as the current Git Extractor.
