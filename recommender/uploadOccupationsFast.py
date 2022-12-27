from py2neo import Graph
from py2neo.bulk import create_nodes, create_relationships
import csv
from itertools import islice

# uri = "neo4j+s://b367eb11.databases.neo4j.io"
# user = "neo4j"
# password = "2WPduo4-J4EK5ZEOuW5cm3hE3ZI85IgaXSOEFTDXHYE"
uri = "neo4j+s://143fd7f8.databases.neo4j.io"
user = "neo4j"
password = "6XbIwSjfgyk6Dr830hsj5ljjS2l66_WKNvxXp5dVlS4"
g = Graph(uri, auth=(user,password), routing=True)

with open('recommender/occupationSkillRelations.csv', encoding='utf-8') as csvfile:
    data = list(csv.reader(csvfile, quotechar=','))
    deduplicatedData = []
    essentialRelationshipData = []
    # optionalRelationshipData = []
    for row in data[1:]:
        deduplicatedData.append(row[0])
        if row[1] == 'essential':
            essentialRelationshipData.append([row[0],{"type":"essential"},row[3]])
        else:
            essentialRelationshipData.append([row[0],{"type":"optional"},row[3]])
    deduplicatedData = list(set(deduplicatedData))
    deduplicatedListData = []
    for row in deduplicatedData:
        deduplicatedListData.append([row])
    keys = ["OccupationUri"]
    create_nodes(g.auto(), deduplicatedListData, labels={"Occupation"}, keys=keys)
    g.nodes.match("Occupation").count()
    stream = iter(essentialRelationshipData)
    batch_size = 5000
    counter = 0
    # print(essentialRelationshipData[0])
    while True:
        batch = islice(stream, batch_size)
        print('current progress: ', counter)
        if batch:
            create_relationships(g.auto(), batch, "requires", \
                start_node_key=("Occupation", "OccupationUri"), end_node_key=("Skill", "concept_uri"))
        else:
            break
        counter += 1
    # create_relationships(g.auto(), essentialRelationshipData, "required", \
        # start_node_key=("Skill", "concept_uri"), end_node_key=("Occupation3", "OccupationUri"))
    # create_relationships(g.auto(), essentialRelationshipData, "ESSENTIAL", \
    #     start_node_key=("Skill", "concept_uri"), end_node_key=("Occupation", "OccupationUri"))
