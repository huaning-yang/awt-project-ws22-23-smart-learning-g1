from urllib.request import urlopen
import json
from classes import person
from classes import job

allskills = ["Java", "JavaScript", "TypeScript",
             "Python", "PHP", "Linux", "Windows", "Docker", "REST"]

link = "https://europa.eu/europass/eportfolio/api/eprofile/shared-profile/253045e3-969d-4882-957d-c68f014e3e6d?view=json"

if link.endswith("html"):
    print("Converting to JSON...")
    link = link.replace("view=html", "view=json")

usersjobs = []
usersskills = []

if not link.startswith("https://europa.eu/europass/eportfolio/api/eprofile/shared-profile/"):
    print("Incorrect link. the only format supported is the europass one. Please go to https://ecas.ec.europa.eu/cas/. Create an account, then create your cv. Finally create an export link to share your cv.")
else:
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
