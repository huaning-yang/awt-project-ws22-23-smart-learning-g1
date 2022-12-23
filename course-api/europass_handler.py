from urllib.request import urlopen
import json
from classes import person
from classes import job

allskills = ["Java", "JavaScript", "TypeScript",
             "Python", "PHP", "Linux", "Windows", "Docker", "REST"]

usersjobs = []
usersskills = []

link = "https://europa.eu/europass/eportfolio/api/eprofile/shared-profile/253045e3-969d-4882-957d-c68f014e3e6d?view=json"
f = urlopen(link)
myfile = f.read()

cvJson = json.loads(myfile)
firstName = cvJson["profile"]["personalInformation"]["firstName"]
lastName = cvJson["profile"]["personalInformation"]["lastName"]
uid = cvJson["profile"]["userId"]

digitalSkills = cvJson["profile"]["digitalSkills"]["other"]
for skill in digitalSkills:
    if skill in allskills:
        usersskills.append(skill)

workExperiences = cvJson["profile"]["workExperiences"]
for experience in workExperiences:
    usersjobs.append(job.Job(experience["occupation"]["label"], str(
        experience["mainActivities"]).replace("<p>", "")))

user1 = person.Person(firstName=firstName, lastName=lastName, id=uid)
user1.skills = usersskills
user1.jobs = usersjobs

user1.print()