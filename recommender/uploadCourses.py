from xml.etree import ElementTree as ET
from tqdm import tqdm
import csv
import pandas as pd
import spacy
import re
import os
from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships
from itertools import islice

tree = ET.parse('input_file')
courses = tree.findall('.//COURSE')

# header = ['course_name', 'course_id', 'course_description']
data = []

for course in courses:
    # name = course.find('CS_NAME').text
    course_id = course.find('CS_ID').text
    location = course.find('CS_LOCATION').text
    datetime = course.find('CS_TIME').text
    # description = course.find('CS_DESC_LONG').text
    # description = description.replace('\\', '')
    dataCourse = [course_id, location, datetime]
    data.append(dataCourse)

uri = "neo4j+s://143fd7f8.databases.neo4j.io"
user = "neo4j"
password = "6XbIwSjfgyk6Dr830hsj5ljjS2l66_WKNvxXp5dVlS4"
g = Graph(uri, auth=(user,password), routing=True)

keys = ["course_id", "course_location", "course_datetime"]
merge_nodes(g.auto(), data, ("Course", "course_id"), keys=keys)