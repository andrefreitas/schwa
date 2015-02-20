class Commit:
    def __init__(self, message, author, timestamp, files):
        self.message = message
        self.author = author
        self.timestamp = timestamp
        self.files = files
