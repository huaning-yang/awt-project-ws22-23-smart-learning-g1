from urllib.request import urlopen
import requests
import json
from classes import person
from classes import job
from classes import skill

#link = "https://europa.eu/europass/eportfolio/api/eprofile/shared-profile/253045e3-969d-4882-957d-c68f014e3e6d?view=json"
link_europass_cv = "https://europa.eu/europass/eportfolio/api/eprofile/shared-profile/7f1bab8d-a88b-4186-bf1d-b78535c740cb?view=html"
essential_url = "http://localhost:5001/occupationessential?"

if link_europass_cv.endswith("html"):
    print("Converting to JSON...")
    link_europass_cv = link_europass_cv.replace("view=html", "view=json")

usersjobs = []
usersskills = []

if not link_europass_cv.startswith("https://europa.eu/europass/eportfolio/api/eprofile/shared-profile/"):
    print("Incorrect link. the only format supported is the europass one. Please go to https://ecas.ec.europa.eu/cas/. Create an account, then create your cv. Finally create an export link to share your cv.")
else:
    f = urlopen(link_europass_cv)
    myfile = f.read()

    cvJson = json.loads(myfile)
    firstName = cvJson["profile"]["personalInformation"]["firstName"]
    lastName = cvJson["profile"]["personalInformation"]["lastName"]
    uid = cvJson["profile"]["userId"]

    competence_uri = "http://localhost:5001/users"

    workExperiences = cvJson["profile"]["workExperiences"]
    for experience in workExperiences:
        occupation = job.Job(experience["occupation"]["label"], str(
            experience["mainActivities"]).replace("<p>", ""))
        if "uri" in experience["occupation"]:
            occupation_uri = experience["occupation"]["uri"]
            occupation.uri = occupation_uri

            PARAMS = {'occupationUri': occupation_uri, "personID": uid}
            response = requests.get(url=essential_url, params=PARAMS)
            data = response.json()
            competencies = []
            for entry in data:
                concept_uri = entry["concept_uri"]
                description = entry["description"]
                preferred_label = entry["preferred_label"]
                competencies.append(preferred_label)
                usersskills.append(skill.Skill(
                    concept_uri, description, preferred_label))

            body = {
                "OccupationUri": occupation_uri,
                "Competencies": competencies
            }
            response_post = requests.post(competence_uri, json=body)
            print(response_post)

        usersjobs.append(occupation)

user1 = person.Person(firstName=firstName, lastName=lastName, id=uid)
user1.skills = usersskills
user1.jobs = usersjobs
user1.print()
