import unittest
from core import *

class TestRepository(unittest.TestCase):

    def testCommitsAndScore(self):
      r = Repository("schwa")
      r.addFile(File("main.java"))
      r.addFile(File("server/clients.java"))
      r.addFile(File("server/products.java"))
      r.commit(Commit("First commit", 123, ["main.java", "server/clients.java", "server/products.java"]))
      r.commit(Commit("Fixed bug #1233", 123, ["main.java"]))
      r.commit(Commit("Fixed bug #3422", 123, ["main.java"]))
      r.commit(Commit("Fixed feature", 123, ["main.java"]))
      print r.rankFiles()

if __name__ == '__main__':
    unittest.main()
