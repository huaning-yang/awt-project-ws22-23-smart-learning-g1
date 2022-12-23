import pandas as pd
from collections import Counter


df = pd.read_csv('occupationSkillRelations.csv')[['occupationUri', 'relationType', 'skillUri']]
df = df[(df['relationType'] == 'essential')]
df = df.drop('relationType', axis=1)
courses = pd.read_csv('all_courses_control.csv')[['course_name','course_id']]
coursesRelations = pd.read_csv('all_relations_NN_control.csv')[['course_id','concept_uri']]
skills = pd.read_csv('skills_de.csv')[['conceptUri','preferredLabel']]

d = df.groupby('occupationUri')['skillUri'].apply(list).to_dict()
coursesToSkills= coursesRelations.groupby('course_id')['concept_uri'].apply(list).to_dict()
skillstoCourses = coursesRelations.groupby('concept_uri')['course_id'].apply(list).to_dict()

d3 = {}
for k in d:
    d2 = {}
    for ele in d[k]:
        d2[ele] = 1
    d3[k] = d2

person = {}
personSkill = {}
for ele in d3['http://data.europa.eu/esco/occupation/207d7b18-6540-432e-8aa6-785ed434572f']:
    if ele != 'http://data.europa.eu/esco/skill/75b30aeb-34c0-40f4-b77d-271d75a98b14' and ele != 'http://data.europa.eu/esco/skill/43d1d56b-ce62-4fe8-8f18-35d92ec73023':
        personSkill[ele]= d3['http://data.europa.eu/esco/occupation/207d7b18-6540-432e-8aa6-785ed434572f'][ele]
    else:
        personSkill[ele] = 0
person['http://data.europa.eu/esco/occupation/207d7b18-6540-432e-8aa6-785ed434572f'] = personSkill
missingSkills = ['http://data.europa.eu/esco/skill/b363bb5f-2c79-40af-94da-33e06f9dee9f']
for k in person['http://data.europa.eu/esco/occupation/207d7b18-6540-432e-8aa6-785ed434572f']:
    if person['http://data.europa.eu/esco/occupation/207d7b18-6540-432e-8aa6-785ed434572f'][k] == 0:
            missingSkills.append(k)
tmp = [skillstoCourses[key] for key in skillstoCourses.keys() if len([keyword for keyword in missingSkills if keyword in key ])>0]
count = Counter(l for llist in tmp for l in llist).most_common(2)

recommendNames = []
recommendSkills = []
for l in count:
    recommendNames.append(courses.loc[courses['course_id'] == l[0]]['course_name'].values[0])


for s in missingSkills:
    recommendSkills.append(skills.loc[skills['conceptUri'] == s]['preferredLabel'].values[0])

print("OCCUPATION DICT")
for k in d:
    print(k)
    print(d[k])
print(f'RECOMMENDATION for Course Names \n {recommendNames}')
print(f'RECOMMENDATION for Competency \n {recommendSkills}')
print(f'Example Person \n {person}')


