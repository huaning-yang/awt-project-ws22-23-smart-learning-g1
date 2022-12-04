# CourseOverview Service

# Import framework
from flask_restful import Resource
from flask import Flask, request, jsonify, g #added to top of file
from flask_cors import CORS #added to top of file
from flask_restful_swagger_2 import Api, swagger, Schema
import sqlite3

from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import Neo4jError
import neo4j.time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

driver = GraphDatabase.driver("neo4j+s://b367eb11.databases.neo4j.io", auth=basic_auth("neo4j", "2WPduo4-J4EK5ZEOuW5cm3hE3ZI85IgaXSOEFTDXHYE"))

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
        result = db.read_transaction(get_courses)
        return [serialize_course(record['course']) for record in result]

# Instantiate the app

api = Api(app)

# # Create routes
# api.add_resource(Course, '/')
# @app.route('/', methods=['GET'])
# def api_get_users():
#     return jsonify(get_courses())

api.add_resource(CourseList, '/')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)