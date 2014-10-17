class File:
  def __init__(self, path):
    self._path = path
    self._commits = []

  def setPath(self, path):
    self._path = path

  def getPath(self):
    return self._path

  def addCommit(self, commit):
    self._commits.append(commit)

  def getCommits(self):
    return self._commits
