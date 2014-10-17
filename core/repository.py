import math

class Repository:
  def __init__(self, name):
    self._name = name
    self._commits = []
    self._files = {}

  def addFile(self, file):
    self._files[file.getPath()] = file

  def getFiles(self):
    return self._files

  def getCommits(self):
    return self._commits

  def commit(self, commit):
    files = commit.getFiles()
    for file in files: #file is the file path, not an istance
      self._files[file].addCommit(commit)
    self._commits.append(commit)

  def rankFiles(self):
    rank = {}
    for filePath in self._files:
      file = self._files[filePath]
      rank[filePath] = self.computeScore(file)
    return rank

  def computeScore(self, file):
    sum = 0
    for commit in file.getCommits():
      if(commit.isBugFixing()):
        ts = commit.getTimeStamp()
        sum += 1 / (1 + math.e**(-12*ts + 12))
    return sum
