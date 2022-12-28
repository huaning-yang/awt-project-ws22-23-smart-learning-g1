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
CORS(app)
api = Api(app)

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
        'summary': 'Find courses filtered by skill',
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
            # For performance reasons limit for now
            return list(tx.run(
                '''
                MATCH (skill:Skill) RETURN skill LIMIT 25
                '''
            ))
        db = get_db()
        result = db.execute_read(get_skills)
        return [serialize_skill(record['skill']) for record in result]

def serialize_skill(skill):
    return {
        'concept_uri': skill['concept_uri'],
        'description': skill['description'],
        'preferred_label': skill['preferred_label']
    }

class OccupationModel(Schema):
    type = 'object'
    properties = {
        'OccupationUri': {
            'type': 'string',
        },
        'preferred_label': {
            'type': 'string',
        }
    }

def serialize_occupation(occupation):
    return {
        'OccupationUri': occupation['OccupationUri'],
        'preferred_label': occupation['preferred_label']
    }

class OccupationList(Resource):
    @swagger.doc({
        'tags': ['occupation'],
        'summary': 'Find all occupations',
        'description': 'Returns a list of occupations',
        'responses': {
            '200': {
                'description': 'A list of occupations',
                'schema': {
                    'type': 'array',
                    'items': OccupationModel,
                }
            }
        }
    })
    def get(self):
        def get_occupations(tx):
            return list(tx.run(
                '''
                MATCH (occupation:Occupation) RETURN occupation LIMIT 25
                '''
            ))
        db = get_db()
        result = db.execute_read(get_occupations)
        return [serialize_occupation(record['occupation']) for record in result]

class ApiDocs(Resource):
    def get(self, path=None):
        if not path:
            path = 'index.html'
        return send_from_directory('swaggerui', path)

api.add_resource(CourseList, '/')
api.add_resource(Courses, '/courses')
api.add_resource(SkillList, '/skills')
api.add_resource(OccupationList, '/occupations')
api.add_resource(ApiDocs, '/docs', '/docs/<path:path>')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)