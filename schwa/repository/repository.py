class Repository:
    def __init__(self, commits, files, timestamp):
        self.commits = commits
        self.timestamp = timestamp
        self.files = files