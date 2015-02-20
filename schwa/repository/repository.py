class Repository:
    def __init__(self, path, commits, files, timestamp):
        self.path = path
        self.commits = commits
        self.files = files
        self.timestamp = timestamp