# Upload Occupation with relations to neo4j
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import csv

class App:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    class OccupationSkillRelation:
        def __init__(self,occupationUriPar,relationTypePar,skillTypePar,skillUriPar)
            self.occupationUri = occupationUriPar
            self.relationType = relationTypePar
            self.skillType = skillTypePar
            self.skillUri = skillUriPar

    def createConstraint():
        query = (
            "CREATE CONSTRAINT ON (o:Occupation) ASSERT o.occupationUri IS UNIQUE"
        )

    def loadCSV();
        with open('occupationSkillRelations.csv') as csvfile:
            return csv.reader(csvfile, quotechar=',')

    def createObjects(data):
        returnList = []
        for row in data:
            returnList.append(OccupationSkillRelation(row['occupationUri'],['relationType'],['skillType'],['skillUri']))
        return returnList

    def createNodes(data):
        query = (
            "CREATE (o:Occupation { occupationUri: $uri }) "
            "RETURN o"
        )
        deduplicatedData = list(set(data['occupationUri']))
        for row in deduplicatedData:
            result = tx.run(query, uri=row)

    def createRelations(data):
        queryEssential = (
            '''
            MATCH (o:Occupation),(s:Skill)
            WHERE o.occupationUri = $oUri AND s.concept_uri = $sUri
            CREATE (s)-[r:ESSENTIAL]->(o)
            RETURN r
            '''
        )
        queryOptional = (
            '''
            MATCH (o:Occupation),(s:Skill)
            WHERE o.occupationUri = $oUri AND s.concept_uri = $sUri
            CREATE (s)-[r:OPTIONAL]->(o)
            RETURN r
            '''
        )
        for row in data:
            query = ''
            if row.relationType = 'essential':
                query = queryEssential
            else:
                query = queryOptional
            result = tx.run(query, oUri=row.occupationUri, sUri=row.skillUri)
            

if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    # driver = GraphDatabase.driver("neo4j+s://b367eb11.databases.neo4j.io", auth=basic_auth("neo4j", "2WPduo4-J4EK5ZEOuW5cm3hE3ZI85IgaXSOEFTDXHYE"))
    # driver = GraphDatabase.driver("neo4j+s://143fd7f8.databases.neo4j.io", auth=basic_auth("neo4j", "6XbIwSjfgyk6Dr830hsj5ljjS2l66_WKNvxXp5dVlS4"))

    uri = "neo4j+s://b367eb11.databases.neo4j.io"
    user = "neo4j"
    password = "2WPduo4-J4EK5ZEOuW5cm3hE3ZI85IgaXSOEFTDXHYE"
    app = App(uri, user, password)
    createConstraint()
    rawData = loadCSV()
    dataObjects = createObjects(rawData)
    createNodes(rawData)

    app.close()