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
        'summary': 'Find courses filtered by skill_name',
        'description': 'Returns a list of courses filtered by skill_name',
        'parameters': [
            {
                'name': 'skill_name',
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
                'description': 'A list of courses filtered by skill_name preferred label',
                'schema': {
                    'type': 'array',
                    'items': CourseModel,
                }
            }
        }
    })
    def get(self):
        skills = request.args.get('skill_name')
        def get_filtered_courses(tx):
            return list(tx.run(
                '''
                MATCH (course:Course)-[:PROVIDE_SKILL]->(skill_name:Skill)
                WHERE skill_name.preferred_label in ["''' + ','.join(skills) +  '''"]
                RETURN course
                '''
            ))

        skills = request.args.getlist('skill_name')
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
        'tags': ['skill_name'],
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
                MATCH (skill_name:Skill) RETURN skill_name LIMIT 25
                '''
            ))
        db = get_db()
        result = db.execute_read(get_skills)
        return [serialize_skill(record['skill_name']) for record in result]

class SkillLabel(Resource):
    @swagger.doc({
        'tags': ['skill_name'],
        'summary': 'find preferred label for a skill_name uri',
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
        'tags': ['skill_name'],
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
                MATCH (course:Course)-[:PROVIDE_SKILL]->(skill_name:Skill)
                WHERE course.course_id in ["''' + ','.join(courses) +  '''"]
                RETURN skill_name
                '''
            ))
        db = get_db()
        result = db.execute_read(get_filtered_skills)
        return [serialize_skill(record['skill_name']) for record in result]

def serialize_skill(skill_name):
    return {
        'concept_uri': skill_name['concept_uri'],
        'description': skill_name['description'],
        'preferred_label': skill_name['preferred_label']
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

class OccupationURI(Resource):
    @swagger.doc({
        'tags': ['occupation'],
        'summary': 'Get occupation URI from preferred label',
        'description': 'Return a uri of a occupation',
        'parameters': [
            {
                'name': 'occupation',
                'description': 'Preferred Label of a occupation',
                'in': 'query',
                'type': 'string'
            }
        ],
        'responses': {
            '200': {
                'description': 'occupation uri',
                'schema': {
                    'type': 'string'
                }
            }
        }
    })
    def get(self):
        label = request.args.getlist('occupation')
        def get_uri(tx):
            return list(tx.run(
                '''
                MATCH (o:Occupation)
                WHERE o.preferred_label in ["''' + ','.join(label) +  '''"]
                RETURN o.OccupationUri
                '''
            ))
        db = get_db()
        result = db.execute_read(get_uri)
        return result

class OccupationEssential(Resource):
    @swagger.doc({
        'tags': ['occupation'],
        'description': 'Returns the essential skills of a occupation',
        'parameters': [
            {
            'name': 'occupationUri',
            'description': 'One occupation (uri) for which the essential skills are needed',
            'in': 'query',
            'type': 'string'
        }],
        'responses': {
            '200': {
                'description': 'list of essential skills',
                'schema': {
                    'type': 'array',
                    'items': 'string'
                }
            }
        }
    })
    def get(self):
        occupation = request.args.getlist('occupationUri')
        def get_essential_skills(tx):
                return list(tx.run(
                '''
                MATCH (o:Occupation)-[r:requires]->(s:Skill)
                WHERE o.OccupationUri in ["''' + ','.join(occupation) +  '''"] AND r.type='essential'
                RETURN s
                '''
            ))
        db = get_db()
        essentials = db.execute_read(get_essential_skills)
        returnSkill = []
        for essential in essentials:
            for sk in essential:
                returnSkill.append(serialize_skill(sk))
        
        return returnSkill

class OccupationOptional(Resource):
    @swagger.doc({
        'tags': ['occupation'],
        'description': 'Returns the optional skills of a occupation',
        'parameters': [
            {
            'name': 'occupationUri',
            'description': 'One occupation (uri) for which the essential skills are needed',
            'in': 'query',
            'type': 'string'
        }],
        'responses': {
            '200': {
                'description': 'list of optional skills',
                'schema': {
                    'type': 'array',
                    'items': 'string'
                }
            }
        }
    })
    def get(self):
        occupation = request.args.getlist('occupationUri')
        def get_optional_skills(tx):
                return list(tx.run(
                '''
                MATCH (o:Occupation)-[r:requires]->(s:Skill)
                WHERE o.OccupationUri in ["''' + ','.join(occupation) +  '''"] AND r.type='optional'
                RETURN s
                '''
            ))
        db = get_db()
        optionals = db.execute_read(get_optional_skills)
        returnSkill = []
        for optional in optionals:
            for sk in optional:
                returnSkill.append(serialize_skill(sk))
        return returnSkill
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
        def get_essentialSkills(tx):
            return list(tx.run(
                '''
                MATCH (o:Occupation)-[:requires]->(s:Skill)
                WHERE o.OccupationUri in ["''' + ','.join(occupation) +  '''"]
                RETURN s
                '''
            ))
        # def get_personSkills(tx):
        #     return list(tx.run(
        #         '''
        #         MATCH (p:person)-[:hasSkill]->(s:skill_name)
        #         WHERE p.id in ["''' + ','.join(personID) +  '''"]
        #         RETURN s
        #         '''
        #     ))
        def get_differences(essential, person):
            return [x for x in essential if x not in person]
        db = get_db()
        essentials = db.execute_read(get_essentialSkills)
        # skills = set(db.execute_read(get_personSkills))
        # return [x for x in essential if x not in skills]
        # essential = ['http://data.europa.eu/esco/skill_name/fed5b267-73fa-461d-9f69-827c78beb39d', 
        # 'http://data.europa.eu/esco/skill_name/05bc7677-5a64-4e0c-ade3-0140348d4125', 
        # 'http://data.europa.eu/esco/skill_name/271a36a0-bc7a-43a9-ad29-0a3f3cac4e57',
        # 'http://data.europa.eu/esco/skill_name/47ed1d37-971b-472c-86be-26f893991274',
        # 'http://data.europa.eu/esco/skill_name/591dd514-735b-46e4-a28d-3a4c42f49b72',
        # 'http://data.europa.eu/esco/skill_name/860be36a-d19b-4ba8-ae74-bc61b9f0bf63',
        # 'http://data.europa.eu/esco/skill_name/93a68dcb-3dc6-4dbe-b196-f6d212228a50',
        # 'http://data.europa.eu/esco/skill_name/f64fe2c2-d090-4e91-ba74-1355d96b9bca'
        # ]

        essentialSkills_uri = []
        for essential in essentials:
            for skill_name in essential:
                essentialSkills_uri.append(skill_name['concept_uri'])
                

        person = ['http://data.europa.eu/esco/skill_name/591dd514-735b-46e4-a28d-3a4c42f49b72',
        'http://data.europa.eu/esco/skill_name/860be36a-d19b-4ba8-ae74-bc61b9f0bf63',
        'http://data.europa.eu/esco/skill_name/93a68dcb-3dc6-4dbe-b196-f6d212228a50',
        'http://data.europa.eu/esco/skill_name/f64fe2c2-d090-4e91-ba74-1355d96b9bca',
        'http://data.europa.eu/esco/skill_name/f64fe2c2-d090-4e91-ba74-1355d96blalbla']

        missing = get_differences(essentialSkills_uri,person)
        returnSkill = []
        for skill_name in missing:
            for essential in essentials:
                for sk in essential:
                    if(sk['concept_uri'] == skill_name):
                        returnSkill.append(serialize_skill(sk))
        return returnSkill


class ApiDocs(Resource):
    def get(self, path=None):
        if not path:
            path = 'index.html'
        return send_from_directory('swaggerui', path)
    

class User(Resource):

    def get(self):
        def get_users(tx):
            return set(tx.run(
                '''
                MATCH (u:User) RETURN u.uid
                '''
            ))
        db = get_db()
        result = flatten(db.execute_read(get_users))
        return result

    def post(self):
        user_arg = reqparse.RequestParser()
        user_arg.add_argument("OccupationUri", type=str, help="This is a node name", required=True)
        user_arg.add_argument("Competencies", action = "append", help="This is a list", required=True)

        competencies = user_arg.parse_args()["Competencies"]
        uri = user_arg.parse_args()["OccupationUri"]
        user_uids = User.get(self)
        uid =  0 if not user_uids else max(user_uids) + 1
        name = f"User {uid}"

        def write_user_occupation(tx, uri, uid, name):
            result = tx.run(
                ''' MATCH (o:Occupation) 
                    WHERE o.OccupationUri = $uri 
                    MERGE (u:User {uid:$uid, name:$name}) -[:planned_occupation]-> (o) 
                    RETURN *
                ''', 
                uri=uri, uid=uid, name=name)
            records = list(result)
            return records
        
        def write_user_competencies(tx, skill_name, uid):
            result = tx.run(
                ''' MATCH (u:User) 
                    WHERE u.uid = $uid
                    MATCH (s:Skill)     
                    WHERE s.preferred_label = $skill_name
                    CREATE (u) -[:hasSkill]-> (s) 
                    RETURN *
                ''', 
                skill_name=skill_name, uid=uid)
            records = list(result)
            return records
        db = get_db()
        db.execute_write(write_user_occupation, uri=uri, uid=uid, name=name)
        [db.execute_write(write_user_competencies, skill_name=skill_name, uid=uid) for skill_name in competencies]
        return {
                "username": name,
                "userUID": uid
        }
    
def flatten(l):
    return [item for sublist in l for item in sublist]   

api.add_resource(CourseList, '/')
api.add_resource(Courses, '/courses')
api.add_resource(SkillList, '/skills')
api.add_resource(Skills, '/filterSkills')
api.add_resource(SkillLabel, '/label')
api.add_resource(MissingEssential, '/essentials')
api.add_resource(OccupationList, '/occupations')
api.add_resource(OccupationURI, '/occupationsuri')
api.add_resource(OccupationEssential, '/occupationessential')
api.add_resource(OccupationOptional, '/occupationoptional')
api.add_resource(ApiDocs, '/docs', '/docs/<path:path>')
api.add_resource(User, '/users')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)