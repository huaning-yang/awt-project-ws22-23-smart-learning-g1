# CourseOverview Service

# Import framework
from time import strftime
from flask_restful import Resource, reqparse
from flask import Flask, request, jsonify, g, send_from_directory #added to top of file
from flask.json import JSONEncoder
from flask_cors import CORS #added to top of file
from flask_restful_swagger_2 import Api, swagger, Schema
from flask_json import FlaskJSON, json_response
import sqlite3
import datetime
import json
from uuid import uuid4

from urllib.request import urlopen
import json

from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import Neo4jError
import neo4j.time

global user_id
user_id = -1

app = Flask(__name__)
# Instantiate the app
CORS(app, resources={r"/*": {"origins": "http://localhost:5002", "headers": "Content-Type, Authorization"}})
# CORS(app)
api = Api(app)

FlaskJSON(app)

@api.representation('application/json')
def output_json(data, code, headers=None):
    return json_response(data_=data, headers_=headers, status_=code)

# driver = GraphDatabase.driver("neo4j+s://b367eb11.databases.neo4j.io", auth=basic_auth("neo4j", "2WPduo4-J4EK5ZEOuW5cm3hE3ZI85IgaXSOEFTDXHYE"))
driver = GraphDatabase.driver("neo4j+s://143fd7f8.databases.neo4j.io", auth=basic_auth("neo4j", "6XbIwSjfgyk6Dr830hsj5ljjS2l66_WKNvxXp5dVlS4"))

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
        },
        'course_location': {
            'type': 'string',
        },
        'course_datetime': {
            'type': 'string',
        }
    }

def serialize_course(course):
    return {
        'course_description': course['course_description'],
        'course_id': course['course_id'],
        'course_name': course['course_name'],
        'course_location': course['course_location'],
        'course_datetime': course['course_datetime'].strftime('%d.%m.%Y') if course['course_datetime'] != datetime.datetime.min else "No dates available"
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
                MATCH (course:Course) RETURN course LIMIT 30
                '''
            ))
        db = get_db()
        result = db.execute_read(get_courses)
        return [serialize_course(record['course']) for record in result]



class Courses(Resource):
    @swagger.doc({
        'tags': ['course'],
        'summary': 'Find courses filtered by skill_uid',
        'description': 'Returns a list of courses filtered by skill_uid',
        'parameters': [
            {
                'name': 'skill_uid',
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
                'description': 'A list of courses filtered by skill_uid',
                'schema': {
                    'type': 'array',
                    'items': CourseModel,
                }
            }
        }
    })
    def get(self):
        skills = request.args.getlist('skill_uid')
        print('''"''' + ''.join(skills) +  '''"''')
        def get_filtered_courses(tx):
            return list(tx.run(
                '''
                MATCH (course:Course)-[:PROVIDE_SKILL]->(s:Skill)
                WHERE s.concept_uri in [''' + ','.join(f'"{sk}"' for sk in skills) +  ''']
                RETURN course
                '''
            ))
        db = get_db()
        result = db.execute_read(get_filtered_courses)
        return [serialize_course(record['course']) for record in result]

class LocationList(Resource):
    @swagger.doc({
        'tags': ['location'],
        'summary': 'Find all locations',
        'description': 'Returns a list of locations',
        'responses': {
            '200': {
                'description': 'A list of locations',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'string',
                    }
                }
            }
        }
    })
    def get(self):
        def get_locations(tx):
            return list(tx.run(
                '''
                MATCH (n:Course) WITH DISTINCT n.course_location AS location
                RETURN location
                '''
            ))
        db = get_db()
        result = db.execute_read(get_locations)
        return [record['location'] for record in result]
        
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
                MATCH (skill_name:Skill) RETURN skill_name LIMIT 30
                '''
            ))
        
        db = get_db()
        result = db.execute_read(get_skills)
        return [serialize_skill(record['skill_name']) for record in result]

class SkillListFilterable(Resource):
    @swagger.doc({
        'tags': ['skill_name'],
        'summary': 'Find all skills',
        'description': 'Returns a list of skills',
        'parameters': [
            {
            'name': 'search',
            'description': 'Search term to filter on',
            'in': 'query',
            'type': 'string'
        }],
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
        searchterm = request.args.get('search')
        if searchterm is None:
            searchterm = ''
        def get_skills(tx):
            # For performance reasons limit for now
            print(searchterm)
            return list(tx.run(
                '''
                MATCH (skill_name:Skill) WHERE skill_name.preferred_label CONTAINS "''' + searchterm +  '''" RETURN skill_name LIMIT 30
                '''
            ))
        
        db = get_db()
        result = db.execute_read(get_skills)
        # return {'items'}
        return {'items': [serialize_skillFilterable(record['skill_name']) for record in result]}

def serialize_skillFilterable(skill_name):
    return {
        'id': skill_name['concept_uri'],
        # 'description': skill_name['description'],
        'text': skill_name['preferred_label']
    }

class OccupationUnobtainableSkills(Resource):
    @swagger.doc({
        'tags': ['occupation'],
        'description': 'Returns list of skills not covered by any courses',
        'parameters': [
            {
            'name': 'occupationUri',
            'description': 'The concept uri of an occupation',
            'in': 'query',
            'type': 'string'
        }],
        'responses': {
            '200': {
                'description': 'list of unobtainable skills',
                'schema': {
                    'type': 'array',
                    'items': 'string'
                }
            }
        }
    })
    def get(self):
        occupation = request.args.getlist('occupationUri')
        def get_unobtainable(tx):
            return list(tx.run(
                '''
                MATCH (o1:Occupation)-[r1:requires {type: 'essential'}]->(s1:Skill) 
                WHERE o1.OccupationUri in ["''' + ','.join(occupation) +  '''"]
                AND NOT ()-[:PROVIDE_SKILL]->(s1) 
                RETURN s1
                '''
            ))
        db = get_db()
        query = db.execute_read(get_unobtainable)
        unobtainable = []
        for sk in query:
            for s in sk:
                unobtainable.append(serialize_skill(s))
        return unobtainable

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
                WHERE course.course_id in [''' + ','.join(f'"{course}"' for course in courses) +  ''']
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
            'description': 'One occupation (uri) for which the essential skills ar e needed',
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

class OccupationRelatedSkills(Resource):
    @swagger.doc({
        'tags': ['occupation'],
        'description': 'Returns a list of skills that are related to the occupation, but not required',
        'parameters': [
            {
            'name': 'occupationUri',
            'description': 'One occupation uri',
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
        def get_relatedSkills(tx):
            return list(tx.run(
                '''
                MATCH (o1:Occupation)-[r1:requires {type: 'essential'}]->(s1:Skill)<-[r2:requires {type: 'essential'}]-(o2:Occupation)-[r3:requires]->(s2:Skill)
                WHERE o1 <> o2 and s1<>s2 AND o1.OccupationUri in ["''' + ','.join(occupation) +  '''"]
                AND NOT (o1)-[:requires]->(s2)
                RETURN s2.preferred_label, count(s2) as s2frequency
                ORDER BY s2frequency DESC
                LIMIT 15
                '''
            ))
        db = get_db()
        relatedSkills = db.execute_read(get_relatedSkills)
        labels = []
        for sk in relatedSkills:
            labels.append(sk[0])
        return labels

class RecommendCoursePath(Resource):
    @swagger.doc({
        'tags': ['recommender'],
        'description': 'Returns list of skills based on which occupation is easiest to archieve',
        'parameters': [
            {
                'name': 'user_uid',
                'description': 'Skillset of a user',
                'in': 'query',
                'type': 'string'
            },
            {
                'name': 'occupation_uri',
                'description': 'Planned occupation',
                'in': 'query',
                'type': 'string'
            }
        ],
        'responses': {
            '200': {
                'description': 'list of courses that one can take to archieve a planned occupation',
                'schema': {
                    'type': 'array',
                    'items': 'string'
                }
            }
        }
    })
    def get(self):
        user_id = request.args.get('user_uid')
        occupation = request.args.get('occupation_uri')
        skills_uri = []
        def get_skillset(tx):
            return list(tx.run(
                '''
                MATCH (u:User)-[r:hasSkill]->(s:Skill)
                WHERE u.uid=$user_id
                RETURN s
                ''', user_id=user_id
            ))
        def get_best_course(tx):
            return list(tx.run(
                '''
                MATCH(c:Course)-[r2:PROVIDE_SKILL]->(m:Skill)<-[r:requires{type: 'essential'}]-(o:Occupation)
                WHERE NOT m.concept_uri in $skills_uri
                AND o.OccupationUri=$occupation
                RETURN c,collect(m.concept_uri), count(m) as freq ORDER by freq DESC LIMIT 2
                ''', skills_uri=skills_uri, occupation=occupation
            ))
        def get_unobtainable(tx):
            return list(tx.run(
                '''
                MATCH (o1:Occupation)-[r1:requires {type: 'essential'}]->(s1:Skill) 
                WHERE o1.OccupationUri=$occupation
                AND NOT ()-[:PROVIDE_SKILL]->(s1) 
                RETURN s1
                ''', occupation=occupation
            ))
        def get_occupation_essential(tx):
            return list(tx.run(
                '''
                MATCH (o:Occupation)-[r:requires {type: 'essential'}]->(s:Skill)
                WHERE o.OccupationUri=$occupation
                RETURN s
                ''', occupation=occupation
            ))

        db = get_db()
        skills = flatten(db.execute_read(get_skillset))
        unobtainable_skills = flatten(db.execute_read(get_unobtainable))
        essentials = flatten(db.execute_read(get_occupation_essential))
        essentials_uri = []
        for sk in essentials:
            essentials_uri.append(sk['concept_uri'])
        for sk in skills:
            skills_uri.append(sk['concept_uri'])
        for sk in unobtainable_skills:
            skills_uri.append(sk['concept_uri'])
        path = []
        while(not all(item in skills_uri for item in essentials_uri)):
            course = flatten(db.execute_read(get_best_course))
            path.append(serialize_course(course[0]))
            path.append(course[1])
            for sk in course[1]:
                skills_uri.append(sk)
        return path

class RecommendBasedOnSkillset(Resource):
    @swagger.doc({
        'tags': ['recommender'],
        'description': 'Returns list of skills based on which occupation is easiest to archieve',
        'parameters': [
            {
                'name': 'user_uid',
                'description': 'Skillset of a user',
                'in': 'query',
                'type': 'string'
            }
        ],
        'responses': {
            '200': {
                'description': 'list of skills that could help achieve occupations',
                'schema': {
                    'type': 'array',
                    'items': 'string'
                }
            }
        }
    })
    def get(self):
        user_uid = request.args.get('user_uid')
        occupation_uri = ''
        def get_occupations_based_on_skill(tx):
            return list(tx.run(
                '''
                MATCH (n:User)-[r:hasSkill]->(s:Skill) 
                WHERE n.uid=$user_uid WITH collect(s) as skills 
                UNWIND skills as m 
                MATCH(o:Occupation)-[r2:requires{type:'essential'}]->(m:Skill) 
                return o,  count(m) as freq ORDER by freq DESC LIMIT 3
                ''', user_uid=user_uid
            ))
        def get_occupation_essential(tx):
            return list(tx.run(
                '''
                MATCH (o:Occupation)-[r:requires {type: 'essential'}]->(s:Skill)
                WHERE o.OccupationUri=$occupation_uri AND NOT s.concept_uri in [''' + ','.join(f'"{skill}"' for skill in skillset_uri) +  ''']
                RETURN s
                ''', occupation_uri=occupation_uri
            ))
        def get_user_skills(tx):
            return list(tx.run(
                '''
                MATCH (u:User)-[r:hasSkill]->(s:Skill)
                WHERE u.uid=$user_uid
                RETURN s
                ''', user_uid=user_uid
            ))
        db = get_db()
        skillset = flatten(db.execute_read(get_user_skills))
        skillset_uri = []
        for sk in skillset:
            uri = sk['concept_uri']
            skillset_uri.append(uri)
        occupations = (db.execute_read(get_occupations_based_on_skill))
        skills = []
        for oc in occupations:
            occupation_uri = oc[0]['OccupationUri']
            occ_skills = flatten(db.execute_read(get_occupation_essential))
            for sk in occ_skills:
                serialized = serialize_skill(sk)
                if serialized not in skills:
                    skills.append(serialized)
        return skills

class RecommenderRankingSkills(Resource):
    @swagger.doc({
        'tags': ['recommender'],
        'description': 'Returns an ordered list of courses based on the skills, location and time',
        'parameters': [
            {
                'name': 'skill_uid',
                'description': 'One or more skills to filter on',
                'in': 'query',
                'type': 'array',
                'items':
                {
                    'type': 'string'
                },
                'collectionFormat': 'multi'
            },
            {
                'name': 'occupationUri',
                'description': 'One occupation uri',
                'in': 'query',
                'type': 'string'
            },
            {
                'name': 'location',
                'description': 'Location of the course',
                'in': 'query',
                'type': 'string'
            },
            {
                'name': 'time',
                'description': 'Enddate of the course',
                'in': 'query',
                'type': 'string'
            }
        ],
        'responses': {
            '200': {
                'description': 'List of course recommendations',
                'schema': {
                    'type': 'array',
                    'items': 'string'
                }
            }
        }
    })
    def get(self):
        skills = request.args.getlist('skill_uid')
        occupation = request.args.getlist('occupationUri')
        location = request.args.get('location')
        time = request.args.get('time')
        course_id = ''
        def get_courses(tx):
            return list(tx.run(
                '''
                MATCH (course:Course)-[:PROVIDE_SKILL]->(s:Skill)
                WHERE s.concept_uri in [''' + ','.join(f'"{sk}"' for sk in skills) +  ''']
                RETURN course
                '''
            ))
        def get_occupation_essential(tx):
            return list(tx.run(
                '''
                MATCH (o:Occupation)-[r:requires]->(s:Skill)
                WHERE o.OccupationUri in ["''' + ','.join(occupation) +  '''"] AND r.type='essential'
                RETURN s
                '''
            ))
        def get_occupation_optional(tx):
            return list(tx.run(
                '''
                MATCH (o:Occupation)-[r:requires]->(s:Skill)
                WHERE o.OccupationUri in ["''' + ','.join(occupation) +  '''"] AND r.type='optional'
                RETURN s
                '''
            ))
        def get_course_skills(tx):
            return list(tx.run(
                '''
                MATCH (course:Course)-[:PROVIDE_SKILL]->(skill_name:Skill)
                WHERE course.course_id=$course_id
                RETURN skill_name
                ''',course_id=course_id
            ))
        def get_course_location(tx):
            return list(tx.run(
                '''
                MATCH (course:Course)
                WHERE course.course_id=$course_id
                RETURN course.course_location
                ''',course_id=course_id
            ))
        def get_course_time(tx):
            return list(tx.run(
                '''
                MATCH (course:Course)
                WHERE course.course_id=$course_id
                RETURN course.course_datetime
                ''',course_id=course_id
            ))
        def get_courses_with_time(tx):
                return list(tx.run(
                '''
                MATCH (course:Course)-[:PROVIDE_SKILL]->(s:Skill)
                WHERE s.concept_uri in [''' + ','.join(f'"{sk}"' for sk in skills) +  '''] AND toString(course.course_datetime) < $time AND toString(course.course_datetime)<>"No dates available" AND toString(course.course_datetime) > toString("0001-01-01T00:00:00")
                RETURN course
                ''',time=time
            ))
        def get_courses_with_location(tx):
                return list(tx.run(
                '''
                MATCH (course:Course)-[:PROVIDE_SKILL]->(s:Skill)
                WHERE s.concept_uri in [''' + ','.join(f'"{sk}"' for sk in skills) +  '''] AND course.course_location=$location
                RETURN course
                ''',location=location
            ))
        def get_courses_with_location_time(tx):
            return list(tx.run(
                '''
                MATCH (course:Course)-[:PROVIDE_SKILL]->(s:Skill)
                WHERE s.concept_uri in [''' + ','.join(f'"{sk}"' for sk in skills) +  '''] AND course.course_location=$location AND toString(course.course_datetime) < $time AND toString(course.course_datetime)<>"No dates available" AND toString(course.course_datetime) > toString("0001-01-01T00:00:00")
                RETURN course
                ''',location=location,time=time
            ))
        def get_course_from_uri(tx):
            return list(tx.run(
                '''
                MATCH (c:Course)
                WHERE c.course_id=$course_id
                RETURN c
                ''', course_id=course_id
            ))
        def compute_score(essentials, optionals, courses):
            number_essentials = len(list(set(essentials).intersection(courses)))
            number_optionals = len(list(set(optionals).intersection(courses)))
            number_irrelevant = len(courses) - len(skills)

            loc_score = 0
            time_score = 0
            if(number_essentials + number_optionals == 0):
                return 0
            location = db.execute_read(get_course_location)
            if(location != 'No location specified'):
                loc_score = 1
            time = db.execute_read(get_course_time)
            if (time != 'No dates available'):
                time_score = 1
            return ((4 * number_essentials) + (2 * number_optionals) + loc_score +  time_score + (0.3 * number_irrelevant)) 
        db = get_db()
        essentials = db.execute_read(get_occupation_essential)
        optionals = db.execute_read(get_occupation_optional)
        if time and location:
            courses = db.execute_read(get_courses_with_location_time)
        elif time and not location:
            courses = db.execute_read(get_courses_with_time)
        elif not time and location:
            courses = db.execute_read(get_courses_with_location)
        else:
            courses = db.execute_read(get_courses)
        essentials_uri = []
        optionals_uri = []
        for tmp in essentials:
            for es in tmp:
                essentials_uri.append(es['concept_uri'])
        for tmp in optionals:
            for op in tmp:
                optionals_uri.append(op['concept_uri'])
        searchedEssentials = list(set(skills).intersection(essentials_uri))
        searchedOptionals = list(set(skills).intersection(optionals_uri))

        courses_skills = {}
        return_dict = {}
        for course in courses:
            for tmp in course:
                course_id = tmp['course_id']
                courses_skills[course_id] = db.execute_read(get_course_skills)
                course_skills_uri = []
                for tmp in courses_skills[course_id]:
                    for test in tmp:
                        course_skills_uri.append(test['concept_uri'])
                return_dict[course_id] = compute_score(searchedEssentials, searchedOptionals, course_skills_uri)
        return_dict = {key:val for key,val in return_dict.items() if val != 0 and key != 'status'}
        sort = sorted(return_dict, key=return_dict.get, reverse=True)[:10]
        course_list = []
        for uri in sort:
            course_id = uri
            course_object = serialize_course(db.execute_read(get_course_from_uri)[0][0])
            course_list.append(course_object)
        return course_list

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
            'name': 'user_id',
            'description': 'Identifier of a person',
            'in': 'query',
            'type': 'integer'
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
        user_uid = request.args.get('user_id')
        def get_essentialSkills(tx):
            return list(tx.run(
                '''
                MATCH (o:Occupation)-[r:requires]->(s:Skill)
                WHERE o.OccupationUri in ["''' + ','.join(occupation) +  '''"] AND r.type='essential'
                RETURN s
                '''
            ))
        def get_personSkills(tx):
            return list(tx.run(
                '''
                MATCH (u:User)-[r:hasSkill]->(s:Skill) 
                WHERE u.uid=$user_uid
                RETURN s
                ''', user_uid=user_uid
            ))
        def get_differences(essential, person):
            return [x for x in essential if x not in person]
        db = get_db()
        essentials = db.execute_read(get_essentialSkills)
        skills = db.execute_read(get_personSkills)
        
        essentialSkills_uri = []
        for essential in essentials:
            for skill_name in essential:
                essentialSkills_uri.append(skill_name['concept_uri'])
                
        person = []
        for sk in skills:
            for s in sk:
                person.append(s['concept_uri'])
        if(skills != []):
            missing = get_differences(essentialSkills_uri,person)
        else:
            missing = essentialSkills_uri
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
    @swagger.doc({
        'tags': ['users'],
        'description': 'Retrieve the uid of the last user in the database',
        'responses': {
            '200': {
                'description': 'Successful retrieval of user uid',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'integer'
                    }
                }
            }
        }
    })
    def get(self):
        user_id_get = request.args.getlist('userID')[0]
        def get_skills(tx, user_id_get):
            result = list(tx.run(

                '''MATCH (u:User)-[r:hasSkill]->(s:Skill) where u.uid=$user_id_get Return collect(s.preferred_label) as preferred_labels''',
                user_id_get=user_id_get
            ))
            return result
        def get_planned_occ(tx, user_id_get):
            result = list(tx.run(

                '''MATCH (u:User)-[r:plannedOccupation]->(o:Occupation) where u.uid=$user_id_get Return collect(o.OccupationUri) as planned_occupation''',
                user_id_get=user_id_get
            ))
            return result
        def get_occupations(tx, user_id_get):
            result = list(tx.run(

                '''MATCH (u:User)-[r:hasOccupation]->(o:Occupation) where u.uid=$user_id_get Return collect(o.OccupationUri) as occupations''',
                user_id_get=user_id_get
            ))
            return result
        db = get_db()
        competencies = db.execute_read(get_skills, user_id_get=user_id_get)
        planned_occ = db.execute_read(get_planned_occ, user_id_get=user_id_get)
        occupations = db.execute_read(get_occupations, user_id_get=user_id_get)
        
        return {
            "preferred_labels": flatten(flatten(competencies)),
            "planned_occupation": flatten(flatten(planned_occ)),
            "occupations": flatten(flatten(occupations))
        }

    
    @swagger.doc({
        'responses': {
            '200': {
                'description': 'Success',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'username': {'type': 'string'},
                        'userUID': {'type': 'string'}
                    }
                }
            },
            '400': {
                'description': 'Bad Request',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        },
        'parameters': [
            {
                'name': 'OccupationUri',
                'in': 'formData',
                'required': True,
                'description': 'This is a node name',
                'type': 'string'
            },
            {
                'name': 'Competencies',
                'in': 'formData',
                'required': True,
                'description': 'This is a list of Competencies',
                'type': 'array',
                'items': {'type': 'string'}
            },
            {
                'name': 'ExistingOccupations',
                'in': 'formData',
                'description': 'This is a list of existing occupations',
                'type': 'array',
                'items': {'type': 'string'}
            }
        ],
        'tags': ['users']
    })
    def post(self):
        user_arg = reqparse.RequestParser()
        user_arg.add_argument("UserID", type=str, help="This is a uuid4 ID", required=True)
        user_arg.add_argument("OccupationUri", type=str, help="This is a node name", required=True)
        user_arg.add_argument("Competencies", action = "append", help="This is a list", required=True)
        user_arg.add_argument("ExistingOccupations", action = "append", help="This is a list")

        competencies = user_arg.parse_args()["Competencies"]
        uri = user_arg.parse_args()["OccupationUri"]
        existing_occupations = user_arg.parse_args()["ExistingOccupations"]
        user_id = user_arg.parse_args()["UserID"]
        
        assert user_id != -1
        uid = user_id
        name = f"User {uid}"

        def delete_old_user(tx, uid):
            user = tx.run(
                '''MATCH (n:User {uid:$uid}) DETACH DELETE n''', 
                uid=uid)
            user = list(user)
            return user
        
        def create_user(tx, uid, name):
            user = tx.run(
                '''CREATE (u:User {uid:$uid, name:$name}) RETURN *''', 
                uid=uid, name=name)
            user = list(user)
            return user
            
        def write_user_occupation(tx, uri, uid):
            result = tx.run(
                ''' MATCH (o:Occupation) 
                    WHERE o.OccupationUri = $uri 
                    MATCH (u:User)
                    WHERE u.uid = $uid
                    MERGE (u) -[:plannedOccupation]-> (o) 
                    RETURN *
                ''', 
                uri=uri, uid=uid)
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
        def write_user_occupations(tx, occupation_uri, uid):
            result = tx.run(
                ''' MATCH (u:User) 
                    WHERE u.uid = $uid
                    MATCH (o:Occupation)     
                    WHERE o.OccupationUri = $occupation_uri
                    CREATE (u) -[:hasOccupation]-> (o) 
                    RETURN *
                ''', 
                occupation_uri=occupation_uri, uid=uid)
            records = list(result)
            return records
        db = get_db()
        db.execute_write(delete_old_user, uid=uid)
        db.execute_write(create_user, uid=uid, name=name)
        db.execute_write(write_user_occupation, uri=uri, uid=uid)
        [db.execute_write(write_user_competencies, skill_name=skill_name, uid=uid) for skill_name in competencies]
        if existing_occupations:
            [db.execute_write(write_user_occupations, occupation_uri=occupation_uri, uid=uid) for occupation_uri in existing_occupations]
        return {
                "username": name,
                "userUID": uid
        }


class Europass(Resource):
    @swagger.doc({
        'tags': ['europass'],
        'description': 'Convert Europass-URL to JSON returning occupations and skills',
        'parameters': [
            {
                'name': 'europassURL',
                'in': 'query',
                'required': True,
                'description': 'The URL of the Europass e-portfolio to be converted to JSON',
                'type': 'string'
            }
        ],
        'responses': {
            '200': {
                'description': 'Success',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'occupations': {'type': 'array'},
                        'preferred_labels': {'type': 'array'}
                    }
                }
            },
            '400': {
                'description': 'Bad Request',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            }
        }      
        
    })
    def get(self):
        europass_url = request.args.getlist('europassURL')[0]
        print(europass_url)
    

        if europass_url.endswith("html"):
            print("Converting to JSON...")
            europass_url = europass_url.replace("view=html", "view=json")

        if not europass_url.startswith("https://europa.eu/europass/eportfolio/api/eprofile/shared-profile/"):
            print(
                "Incorrect link. the only format supported is the europass one. Please go to https://ecas.ec.europa.eu/cas/. Create an account, then create your cv. Finally create an export link to share your cv.")
        else:
            f = urlopen(europass_url)
            myfile = f.read()

            cvJson = json.loads(myfile)

            # collect occupations
            occs = []

            workExperiences = cvJson["profile"]["workExperiences"]
            for experience in workExperiences:

                if "uri" in experience["occupation"]:
                    occupation = experience["occupation"]["uri"]
                    occupation_uri = str(occupation)
                    occupation_uri_lst = [str(occupation)]
                
                occs.append(occupation_uri) if not occupation_uri == "None" else None

                def get_essential_skills(tx):
                            return list(tx.run(
                            '''
                            MATCH (o:Occupation)-[r:requires]->(s:Skill)
                            WHERE o.OccupationUri in ["''' + ','.join(occupation_uri_lst) +  '''"] AND r.type='essential'
                            RETURN s
                            '''
                        ))

                db = get_db()
                essentials = db.execute_read(get_essential_skills)

                competencies = []
                for essential in essentials:
                    for sk in essential:
                        competencies.append(serialize_skill(sk))

                preferred_labels = []
                for c in competencies:
                    preferred_labels.append(c["preferred_label"])

        return {
                "occupations": occs,
                "preferred_labels": preferred_labels
                }
    
class UserID(Resource):

    def get(self):
        global user_id
        user_id = str(uuid4())
        return {
            "userID": user_id
        }

def flatten(l):
    return [item for sublist in l for item in sublist]

api.add_resource(CourseList, '/')
api.add_resource(Courses, '/courses')
api.add_resource(SkillList, '/skills')
api.add_resource(SkillListFilterable, '/skillsFilterable')
api.add_resource(Skills, '/filterSkills')
api.add_resource(SkillLabel, '/label')
api.add_resource(RecommenderRankingSkills, '/rankingSkills')
api.add_resource(MissingEssential, '/essentials')
api.add_resource(OccupationList, '/occupations')
api.add_resource(OccupationURI, '/occupationsuri')
api.add_resource(OccupationUnobtainableSkills, '/occupationunobtainable')
api.add_resource(OccupationEssential, '/occupationessential')
api.add_resource(OccupationOptional, '/occupationoptional')
api.add_resource(RecommendCoursePath, '/coursePath')
api.add_resource(RecommendBasedOnSkillset, '/recommendSkillset')
api.add_resource(OccupationRelatedSkills, '/occupationrelated')
api.add_resource(ApiDocs, '/docs', '/docs/<path:path>')
api.add_resource(User, '/users')
api.add_resource(Europass, '/europass')
api.add_resource(LocationList, '/locations')
api.add_resource(UserID, '/userid')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)