from xml.etree import ElementTree as ET
from tqdm import tqdm
import csv
import pandas as pd
import spacy
import re
import os
from py2neo import Graph
from py2neo.bulk import merge_nodes, create_relationships
from datetime import datetime

tree = ET.parse("C:/Users/Oscar/iCloudDrive/2022-11-02_FOKUS_AWT_CompetencyExtraction_WB_Brandenburg_re-encoded - Kopie.xml")
courses = tree.findall('.//COURSE')

# header = ['course_name', 'course_id', 'course_description']
data = []

for course in courses:
    # name = course.find('CS_NAME').text
    course_id = course.find('CS_ID').text
    schedules = course.findall("./COURSESCHEDULES/SCHEDULE")
    if len(schedules) > 0:
        if schedules[0].find('./ADDRESS/A_CITY') is not None:
            location = schedules[0].find('./ADDRESS/A_CITY').text
        else:
            location = "No location specified"
        if schedules[0].find('S_END_DATE') is not None:
            datetime = datetime.strptime(schedules[0].find('S_END_DATE').text, '%Y-%m-%dT%H:%M:%S')
        else:
            datetime = datetime.min
    else:
        location = "No location specified"
        datetime = datetime.min
    # description = course.find('CS_DESC_LONG').text
    # description = description.replace('\\', '')
    dataCourse = [course_id, location, datetime]
    data.append(dataCourse)
    # print(dataCourse)

uri = "neo4j+s://143fd7f8.databases.neo4j.io"
user = "neo4j"
password = "6XbIwSjfgyk6Dr830hsj5ljjS2l66_WKNvxXp5dVlS4"
g = Graph(uri, auth=(user,password), routing=True)

keys = ["course_id", "course_location", "course_datetime"]
merge_nodes(g.auto(), data, ("Course", "course_id"), keys=keys)