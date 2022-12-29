from py2neo import Graph
from py2neo.bulk import merge_nodes
import csv


# uri = "neo4j+s://b367eb11.databases.neo4j.io"
# user = "neo4j"
# password = "2WPduo4-J4EK5ZEOuW5cm3hE3ZI85IgaXSOEFTDXHYE"
uri = "neo4j+s://143fd7f8.databases.neo4j.io"
user = "neo4j"
password = "6XbIwSjfgyk6Dr830hsj5ljjS2l66_WKNvxXp5dVlS4"
g = Graph(uri, auth=(user,password), routing=True)

with open('recommender/occupations_de.csv', encoding='utf-8') as csvfile:
    data = list(csv.reader(csvfile, quotechar='"',))
    uploadData = []
    for row in data[1:]:
        if row[0] == 'Occupation':
            uploadData.append([row[1],row[3]])
    keys = ["OccupationUri","preferred_label"]
    merge_nodes(g.auto(), uploadData, merge_key=("Occupation","OccupationUri"), labels={"Occupation", "OccupationUri", "preferred_label"}, keys=keys)
    print(g.nodes.match("Occupation").count())
    