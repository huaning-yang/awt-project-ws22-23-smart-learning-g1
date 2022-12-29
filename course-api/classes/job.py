class Job:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.uri = ""

    def print(self):
        print(f"   - Job title: {self.title}")
        print(f"       Job description: {self.description}")
