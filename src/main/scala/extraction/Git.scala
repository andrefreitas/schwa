package extraction

import java.io._
import org.eclipse.jgit.storage.file.FileRepositoryBuilder
import org.eclipse.jgit.lib.Repository
import org.eclipse.jgit.lib.Ref
import org.eclipse.jgit.revwalk.RevWalk
import org.eclipse.jgit.revwalk.RevCommit
import org.eclipse.jgit.revwalk.RevTree
import org.eclipse.jgit.treewalk.TreeWalk

class Git(_path: String) {
  var path: String = _path
  val builder: FileRepositoryBuilder = new FileRepositoryBuilder()
  val repository: Repository = builder.setGitDir(new File(path)).readEnvironment().findGitDir().build()

  def getFiles(){
    val head: Ref = repository.getRef("head")
    val walk:RevWalk = new RevWalk(repository)
    val commit:RevCommit  = walk.parseCommit(head.getObjectId())
    val tree:RevTree = commit.getTree()

    val treeWalk:TreeWalk = new TreeWalk(repository)
    treeWalk.addTree(tree)
    treeWalk.setRecursive(true)
    while(treeWalk.next()){
      println(treeWalk.getPathString())
    }

  }
}
