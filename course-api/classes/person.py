from classes.job import Job


class Person:
    def __init__(self, firstName, lastName, id):
        self.firstName = firstName
        self.lastName = lastName
        self.id = id
        self.jobs = []
        self.skills = []

    def print(self):
        print(f"User name: {self.firstName} {self.lastName}")
        print(f"User ID: {self.id}")
        print("Jobs:----")
        for job in self.jobs:
            job.print()
        print(f"Skills:----)")
        for skill in self.skills:
            skill.print()
