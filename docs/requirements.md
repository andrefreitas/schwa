# Requirements report
## 1. Glossary
Term  | Description
------------- | -------------
Bug | Deviation of a program from its expected result.
Defect  | An error created by a programmer when writing code.
Crowbar | A tool that uses fault localization available at www.crowbar.io

## 2. Introduction
In this document, the project is described along with its requirements and domain model.

## 3. Project
Software debugging have a big impact in Software development costs. Developers need to focus their resources to fix defects faster, by knowing the components that are more faulty. Schwa is a project that aims to give defects information, by Mining Software Repositories. Existing fault localization tools can benefit from Schwa defect probabilities (a priori), such as Crowbar.

## 4. Requirements
### 4.1 Actors
Name | Description
------------- | -------------
Developer | Is a Software Engineer that needs Schwa to track defects.
Crowbar | Is a tool that relies on Schwa to obtain defect probabilities.

### 4.2 Functional requirements

ID  | Name | Description | Points | Priority
------------- | -------------
US01  | GIT repositories | As a developer, I can analyze Git repositories, because is the most popular CVS.  | 5 | High
US02  | Java Projects | As a developer, I can analyze my Java projects, because is a popular programming language. | 8 | High
US03 | Interface | As a developer, I can invoke Schwa by command line and get a Sunburst chart, because is an effective way of displaying defects. | 3 | Medium

### 4.3 Non-functional requirements
ID  | Name | Description
------------- | -------------
R01  | Performance | It should scale to big repositories.


## 5. Domain model
