from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships
import csv

uri = "neo4j+s://b367eb11.databases.neo4j.io"
user = "neo4j"
password = "2WPduo4-J4EK5ZEOuW5cm3hE3ZI85IgaXSOEFTDXHYE"
# uri = "neo4j+s://143fd7f8.databases.neo4j.io"
# user = "neo4j"
# password = "6XbIwSjfgyk6Dr830hsj5ljjS2l66_WKNvxXp5dVlS4"
g = Graph(uri, auth=(user,password), routing=True)

with open('recommender\occupationSkillRelations.csv', encoding='utf-8') as csvfile:
    data = list(csv.reader(csvfile, quotechar=','))
    deduplicatedData = []
    essentialRelationshipData = []
    # optionalRelationshipData = []
    for row in data[1:]:
        deduplicatedData.append(row[3])
        if row[1] == 'essential':
            essentialRelationshipData.append([row[3],{"type":"essential"},row[0]])
        else:
            essentialRelationshipData.append([row[3],{"type":"optional"},row[0]])
    deduplicatedData = list(set(deduplicatedData))
    deduplicatedListData = []
    for row in deduplicatedData:
        deduplicatedListData.append([row])
    keys = ["OccupationUri"]
    create_nodes(g.auto(), deduplicatedListData, labels={"Occupation2"}, keys=keys)
    g.nodes.match("Occupation").count()
    
    create_relationships(g.auto(), essentialRelationshipData, "required", \
        start_node_key=("Skill", "concept_uri"), end_node_key=("Occupation", "OccupationUri"))
    # create_relationships(g.auto(), essentialRelationshipData, "ESSENTIAL", \
    #     start_node_key=("Skill", "concept_uri"), end_node_key=("Occupation", "OccupationUri"))
