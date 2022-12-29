# Upload Occupation with relations to neo4j
from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import csv

class OccupationSkillRelation:
    def __init__(self,occupationUriPar,relationTypePar,skillTypePar,skillUriPar):
        self.occupationUri = occupationUriPar
        self.relationType = relationTypePar
        self.skillType = skillTypePar
        self.skillUri = skillUriPar

class App:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def createConstraint(self):
        with self.driver.session() as session:
            result = session.execute_write(self._create_cosntraint_occupation)

    @staticmethod
    def _create_cosntraint_occupation(tx):
        result = tx.run("CREATE CONSTRAINT FOR (o:Occupation) REQUIRE o.occupationUri IS UNIQUE")
        return result

    def createObjects(self):
        returnList = []
        with open('recommender\occupationSkillRelations.csv', encoding='utf-8') as csvfile:
            data = csv.DictReader(csvfile, quotechar=',')
            for row in data:
                returnList.append(OccupationSkillRelation(row['occupationUri'],['relationType'],['skillType'],['skillUri']))
        return returnList

    def createNodes(self):
        """Read csv file and create nodes for occupations"""
        with open('recommender\occupationSkillRelations.csv', encoding='utf-8') as csvfile:
            data = list(csv.reader(csvfile, quotechar=','))
            deduplicatedData = []
            print(len(data))
            for row in data[1:]:
                deduplicatedData.append(row[3])
            deduplicatedData = list(set(deduplicatedData))
            print(len(deduplicatedData))
            with self.driver.session() as session:
                for row in deduplicatedData:
                    # result = ''
                    result = session.execute_write(self._create_nodes, row)

    @staticmethod
    def _create_nodes(tx,data):
        query = (
            "CREATE (o:Occupation { occupationUri: $uri }) "
            "RETURN o"
        )
        result = tx.run(query, uri=data)
        return result

    def createRelations(self,data):
        with self.driver.session() as session:
            for row in data:   
                # result = ''
                result = session.execute_write(self._create_relations, row)

    @staticmethod
    def _create_relations(tx,data):
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
        query = ''
        if data.relationType == 'essential':
            query = queryEssential
        else:
            query = queryOptional
        result = tx.run(query, oUri=data.occupationUri, sUri=data.skillUri)
        return result
        
if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    # driver = GraphDatabase.driver("neo4j+s://b367eb11.databases.neo4j.io", auth=basic_auth("neo4j", "2WPduo4-J4EK5ZEOuW5cm3hE3ZI85IgaXSOEFTDXHYE"))
    # driver = GraphDatabase.driver("neo4j+s://143fd7f8.databases.neo4j.io", auth=basic_auth("neo4j", "6XbIwSjfgyk6Dr830hsj5ljjS2l66_WKNvxXp5dVlS4"))

    uri = "neo4j+s://b367eb11.databases.neo4j.io"
    user = "neo4j"
    password = "2WPduo4-J4EK5ZEOuW5cm3hE3ZI85IgaXSOEFTDXHYE"
    # uri = "neo4j+s://143fd7f8.databases.neo4j.io"
    # user = "neo4j"
    # password = "6XbIwSjfgyk6Dr830hsj5ljjS2l66_WKNvxXp5dVlS4"
    app = App(uri, user, password)
    # app.createConstraint()
    print("Creating objects")
    dataObjects = app.createObjects()
    print("Creating nodes")
    app.createNodes()
    print("Creating relations")
    app.createRelations(dataObjects)
    app.close()