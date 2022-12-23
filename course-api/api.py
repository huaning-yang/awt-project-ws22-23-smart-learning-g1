# CourseOverview Service

# Import framework
from flask_restful import Resource, reqparse
from flask import Flask, request, jsonify, g, send_from_directory #added to top of file
from flask_cors import CORS #added to top of file
from flask_restful_swagger_2 import Api, swagger, Schema
from flask_json import FlaskJSON, json_response
import sqlite3

from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import Neo4jError
import neo4j.time

app = Flask(__name__)
# Instantiate the app

api = Api(app)
CORS(app)
FlaskJSON(app)

@api.representation('application/json')
def output_json(data, code, headers=None):
    return json_response(data_=data, headers_=headers, status_=code)

# driver = GraphDatabase.driver("neo4j+s://b367eb11.databases.neo4j.io", auth=basic_auth("neo4j", "2WPduo4-J4EK5ZEOuW5cm3hE3ZI85IgaXSOEFTDXHYE"))
driver = GraphDatabase.driver("neo4j+s://143fd7f8.databases.neo4j.io", auth=basic_auth("neo4j", "6XbIwSjfgyk6Dr830hsj5ljjS2l66_WKNvxXp5dVlS4"))


def get_db_connection():
    conn = sqlite3.connect('/usr/src/app/data/database.db')
    conn.row_factory = sqlite3.Row
    return conn


# def get_courses():
#     courses = []
#     try:
#         conn = get_db_connection()
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM courses")
#         rows = cur.fetchall()

#         # convert row objects to dictionary
#         for i in rows:
#             course = {}
#             course["CS_NAME"] = i["CS_NAME"]
#             course["CS_ID"] = i["CS_ID"]
#             course["CS_LANGUAGE"] = i["CS_LANGUAGE"]
#             course["CS_SUPPLIERID"] = i["CS_SUPPLIERID"]
#             course["CS_DEGREE_EXAM"] = i["CS_DEGREE_EXAM"]
#             course["CS_PRICE"] = i["CS_PRICE"]
#             course["CS_WDB_TYPE"] = i["CS_WDB_TYPE"]
#             course["CS_WDB_MODE"] = i["CS_WDB_MODE"]
#             course["CS_WDB_UNTERRICHTSSTUNDEN_ANZAHL"] = i["CS_WDB_UNTERRICHTSSTUNDEN_ANZAHL"]
#             courses.append(course)
#     except:
#         courses = []

#     return courses

def get_db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session()
    return g.neo4j_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'neo4j_db'):
        g.neo4j_db.close()


class CourseModel(Schema):
    type = 'object'
    properties = {
        'course_description': {
            'type': 'string',
        },
        'course_id': {
            'type': 'string',
        },
        'course_name': {
            'type': 'string',
        }
    }

def serialize_course(course):
    return {
        'course_description': course['course_description'],
        'course_id': course['course_id'],
        'course_name': course['course_name']
    }

class CourseList(Resource):
    @swagger.doc({
        'tags': ['course'],
        'summary': 'Find all courses',
        'description': 'Returns a list of courses',
        'responses': {
            '200': {
                'description': 'A list of courses',
                'schema': {
                    'type': 'array',
                    'items': CourseModel,
                }
            }
        }
    })
    def get(self):
        def get_courses(tx):
            return list(tx.run(
                '''
                MATCH (course:Course) RETURN course
                '''
            ))
        db = get_db()
        result = db.execute_read(get_courses)
        return [serialize_course(record['course']) for record in result]



class Courses(Resource):
    @swagger.doc({
        'tags': ['course'],
        'summary': 'Find courses filtered by skill prefered label',
        'description': 'Returns a list of courses filtered by skill',
        'parameters': [
            {
                'name': 'skill',
                'description': 'One or more skills to filter on',
                'in': 'query',
                'type': 'array',
                'items':
                {
                    'type': 'string'
                },
                'collectionFormat': 'multi'
            }
        ],
        'responses': {
            '200': {
                'description': 'A list of courses filtered by skill',
                'schema': {
                    'type': 'array',
                    'items': CourseModel,
                }
            }
        }
    })
    def get(self):
        skills = request.args.get('skill')
        def get_filtered_courses(tx):
            return list(tx.run(
                '''
                MATCH (course:Course)-[:PROVIDE_SKILL]->(skill:Skill)
                WHERE skill.preferred_label in ["''' + ','.join(skills) +  '''"]
                RETURN course
                '''
            ))

        skills = request.args.getlist('skill')
        print(skills)
        # return(skills)
        db = get_db()
        result = db.execute_read(get_filtered_courses)
        return [serialize_course(record['course']) for record in result]
        
class SkillModel(Schema):
    type = 'object'
    properties = {
        'concept_uri': {
            'type': 'string',
        },
        'description': {
            'type': 'string',
        },
        'preferred_label': {
            'type': 'string',
        }
    }

class SkillLabel(Resource):
    @swagger.doc({
        'tags': ['skill'],
        'summary': 'find preferred label for a skill uri',
        'description': 'return a preferred label for list of skills',
        'parameters': [
            {
                'name': 'skilluri',
                'in': 'query',
                'type': 'string'
            }
        ],
        'responses': {
            '200':{
                'description': 'A list of pref label skills',
                'schema': {
                    'type': 'string'
                }
            }
        }
    })
    def get(self):
        skills = request.args.getlist('skilluri')
        def get_pref_label(tx):
            return list(tx.run(
                '''
                MATCH (s:Skill)
                WHERE s.concept_uri in ["''' + ','.join(skills) +  '''"]
                RETURN s.preferred_label'''
            ))
        db = get_db()
        result = db.execute_read(get_pref_label)
        return result[0]

class Skills(Resource):
    @swagger.doc({
        'tags': ['skill'],
        'summary': 'Find skills filtered by course id',
        'description': 'Returns a list of skills filtered by courses',
        'parameters': [
            {
                'name': 'course',
                'description': 'One or more course ids to filter on',
                'in': 'query',
                'type': 'array',
                'items':
                {
                    'type': 'string'
                },
                'collectionFormat': 'multi'
            }
        ],
        'responses': {
            '200': {
                'description': 'A list of skills filtered by courses',
                'schema': {
                    'type': 'array',
                    'items': SkillModel,
                }
            }
        }
    })
    def get(self):
        courses = request.args.getlist('course')
        def get_filtered_skills(tx):
            return list(tx.run(
                '''
                MATCH (course:Course)-[:PROVIDE_SKILL]->(skill:Skill)
                WHERE course.course_id in ["''' + ','.join(courses) +  '''"]
                RETURN skill
                '''
            ))
        db = get_db()
        result = db.execute_read(get_filtered_skills)
        return [serialize_skill(record['skill']) for record in result]
class SkillList(Resource):
    @swagger.doc({
        'tags': ['skill'],
        'summary': 'Find all skills',
        'description': 'Returns a list of skills',
        'responses': {
            '200': {
                'description': 'A list of skills',
                'schema': {
                    'type': 'array',
                    'items': SkillModel,
                }
            }
        }
    })
    def get(self):
        def get_skills(tx):
            return list(tx.run(
                '''
                MATCH (skill:Skill) RETURN skill
                '''
            ))
            # return list(tx.run(
            #     '''
            #     MATCH (course:Course)-[:PROVIDE_SKILL]->(skill:Skill)
            #     WHERE course.course_name in ['Social-Media Manager','Webentwicklung 2.0 - HTML5, CSS3, WordPress','Weiterbildung Wildnispädagogik','Programmierung PHP Frameworks: Laravel, Symfony, Zend','Experte in Investition und Finanzierung']
            #     RETURN skill
            #     '''
            # ))
        db = get_db()
        result = db.execute_read(get_skills)
        return [serialize_skill(record['skill']) for record in result]

def serialize_skill(skill):
    return {
        'concept_uri': skill['concept_uri'],
        'description': skill['description'],
        'preferred_label': skill['preferred_label']
    }

class MissingEssential(Resource):
    @swagger.doc({
        'tags': ['recommender'],
        'description': 'Recommends keywords based on rules using missing essential skills',
        'parameters': [
            {
            'name': 'occupationUri',
            'description': 'One or more Occupations (uri) to recommend missing skills',
            'in': 'query',
            'type': 'array',
            'items': {
                'type': 'string'
            },
            'collectionFormat': 'multi'
        },
        {
            'name': 'personID',
            'description': 'Identifier of a person',
            'in': 'query',
            'type': 'string'
        }],
        'responses': {
            '200': {
                'description': 'list of missing skills',
                'schema': {
                    'type': 'array',
                    'items': 'string'
                }
            }
        }
    })
    def get(self):
        occupation = request.args.getlist('occupationUri')
        personID = request.args.getlist('personID')
        # def get_essentialSkills(tx):
        #     return list(tx.run(
        #         '''
        #         MATCH (o:Occupation)-[:essential]->(s:Skill)
        #         WHERE o.occupationURI in ["''' + ','.join(occupation) +  '''"]
        #         RETURN s
        #         '''
        #     ))
        # def get_personSkills(tx):
        #     return list(tx.run(
        #         '''
        #         MATCH (p:person)-[:hasSkill]->(s:skill)
        #         WHERE p.id in ["''' + ','.join(personID) +  '''"]
        #         RETURN s
        #         '''
        #     ))
        def get_differences(essential, person):
            return [x for x in essential if x not in person]
        #db = get_db()
        # essential = db.execute_read(get_essentialSkills)
        # skills = set(db.execute_read(get_personSkills))
        # return [x for x in essential if x not in skills]
        essential = ['http://data.europa.eu/esco/skill/fed5b267-73fa-461d-9f69-827c78beb39d', 
        'http://data.europa.eu/esco/skill/05bc7677-5a64-4e0c-ade3-0140348d4125', 
        'http://data.europa.eu/esco/skill/271a36a0-bc7a-43a9-ad29-0a3f3cac4e57',
        'http://data.europa.eu/esco/skill/47ed1d37-971b-472c-86be-26f893991274',
        'http://data.europa.eu/esco/skill/591dd514-735b-46e4-a28d-3a4c42f49b72',
        'http://data.europa.eu/esco/skill/860be36a-d19b-4ba8-ae74-bc61b9f0bf63',
        'http://data.europa.eu/esco/skill/93a68dcb-3dc6-4dbe-b196-f6d212228a50',
        'http://data.europa.eu/esco/skill/f64fe2c2-d090-4e91-ba74-1355d96b9bca'
        ]

        person = ['http://data.europa.eu/esco/skill/591dd514-735b-46e4-a28d-3a4c42f49b72',
        'http://data.europa.eu/esco/skill/860be36a-d19b-4ba8-ae74-bc61b9f0bf63',
        'http://data.europa.eu/esco/skill/93a68dcb-3dc6-4dbe-b196-f6d212228a50',
        'http://data.europa.eu/esco/skill/f64fe2c2-d090-4e91-ba74-1355d96b9bca',
        'http://data.europa.eu/esco/skill/f64fe2c2-d090-4e91-ba74-1355d96blalbla']

        missing = get_differences(essential,person)
        return missing
        

class ApiDocs(Resource):
    def get(self, path=None):
        if not path:
            path = 'index.html'
        return send_from_directory('swaggerui', path)



# # Create routes
# api.add_resource(Course, '/')
# @app.route('/', methods=['GET'])
# def api_get_users():
#     return jsonify(get_courses())

api.add_resource(CourseList, '/')
api.add_resource(Courses, '/courses')
api.add_resource(SkillList, '/skills')
api.add_resource(Skills, '/filterSkills')
api.add_resource(SkillLabel, '/label')
api.add_resource(MissingEssential, '/essentials')
api.add_resource(ApiDocs, '/docs', '/docs/<path:path>')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)