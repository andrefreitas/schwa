import re

class Commit:
  def __init__(self, message, timeStamp, files):
    self._message = message
    self._timeStamp = timeStamp
    self._files = files

  def setMessage(self, message):
    self._message = message

  def getMessage(self):
    return self._message

  def setTimeStamp(self, timeStamp):
    self._timeStamp = timeStamp

  def getTimeStamp(self):
    return self._timeStamp

  def setFiles(self, files):
    self._files = files

  def getFiles(self):
    return self._files

  def isBugFixing(self):
    return re.search("bug", self.getMessage(), re.I) != None
