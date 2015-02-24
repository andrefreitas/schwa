class Commit:
    def __init__(self, _id, message, author, timestamp, files_ids):
        self._id = _id
        self.message = message
        self.author = author
        self.timestamp = timestamp
        self.files_ids = files_ids

