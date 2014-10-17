import math

class Repository:
  def __init__(self, name, timeStamp):
    self._timeStamp = timeStamp
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

  def rankFiles(self, timeStampNow):
    rank = {}
    for filePath in self._files:
      file = self._files[filePath]
      rank[filePath] = self.computeScore(file, timeStampNow)
    return rank

  def computeScore(self, file, timeStampNow):
    sum = 0
    for commit in file.getCommits():
      if(commit.isBugFixing()):
        ts = commit.getTimeStamp()
        ts = self.normalizeTimeStamp(ts, timeStampNow)
        sum += 1 / (1 + math.e**(-12*ts + 12))
    return sum

  def normalizeTimeStamp(self, ts, tsNow):
    diffBegin = ts - self._timeStamp
    diff = tsNow - ts
    normalized = diffBegin / float(diff)
    return normalized
