from urllib.request import urlopen
import requests
import json
from classes import person
from classes import job
from classes import skill

allskills = ["Java", "JavaScript", "TypeScript",
             "Python", "PHP", "Linux", "Windows", "Docker", "REST"]

link = "https://europa.eu/europass/eportfolio/api/eprofile/shared-profile/253045e3-969d-4882-957d-c68f014e3e6d?view=json"
# link = "https://europa.eu/europass/eportfolio/api/eprofile/shared-profile/7f1bab8d-a88b-4186-bf1d-b78535c740cb?view=html"
swagger_url = "http://localhost:5001/essentials?"

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

    workExperiences = cvJson["profile"]["workExperiences"]
    for experience in workExperiences:
        occupation = job.Job(experience["occupation"]["label"], str(
            experience["mainActivities"]).replace("<p>", ""))
        if "uri" in experience["occupation"]:
            occupation_uri = experience["occupation"]["uri"]
            occupation.uri = occupation_uri

            PARAMS = {'occupationUri': occupation_uri}
            response = requests.get(url=swagger_url, params=PARAMS)
            data = response.json()

            for entry in data:
                concept_uri = entry["concept_uri"]
                description = entry["description"]
                preferred_label = entry["preferred_label"]
                usersskills.append(skill.Skill(
                    concept_uri, description, preferred_label))
        usersjobs.append(occupation)

    user1 = person.Person(firstName=firstName, lastName=lastName, id=uid)
    user1.skills = usersskills
    user1.jobs = usersjobs

    user1.print()
