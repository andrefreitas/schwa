import unittest
from core import *

class TestCommit(unittest.TestCase):

    def testSetAndGet(self):
      f = "Clients.java"
      c = Commit("Fixed bug #1234", 1234, [f])
      self.assertEqual("Fixed bug #1234", c.getMessage())
      self.assertEqual(1234, c.getTimeStamp())
      self.assertEqual([f], c.getFiles())

    def testBug(self):
      f = "Clients.java"
      c = Commit("Fixed bug #1234", 1234, [f])
      self.assertEqual(True, c.isBugFixing())
      c = Commit("Implemented feature #532", 2234, [f])
      self.assertEqual(False, c.isBugFixing())



if __name__ == '__main__':
    unittest.main()
