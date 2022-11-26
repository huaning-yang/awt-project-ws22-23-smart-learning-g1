# CourseOverview Service

# Import framework
from flask_restful import Resource, Api
from flask import Flask, request, jsonify #added to top of file
from flask_cors import CORS #added to top of file
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('/usr/src/app/data/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_courses():
    courses = []
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM courses")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            course = {}
            course["CS_NAME"] = i["CS_NAME"]
            course["CS_ID"] = i["CS_ID"]
            course["CS_LANGUAGE"] = i["CS_LANGUAGE"]
            course["CS_SUPPLIERID"] = i["CS_SUPPLIERID"]
            course["CS_DEGREE_EXAM"] = i["CS_DEGREE_EXAM"]
            course["CS_PRICE"] = i["CS_PRICE"]
            course["CS_WDB_TYPE"] = i["CS_WDB_TYPE"]
            course["CS_WDB_MODE"] = i["CS_WDB_MODE"]
            course["CS_WDB_UNTERRICHTSSTUNDEN_ANZAHL"] = i["CS_WDB_UNTERRICHTSSTUNDEN_ANZAHL"]
            courses.append(course)
    except:
        courses = []

    return courses

# @dataclass
# class Course(Resource):
#     def get(self):
#         return {
#             'Courses': ['Aktuelles Arbeitsrecht 2022', 'Ambulante Pflege - Rechtssicher Handeln und Haftungsrisiken vermeiden', 
#             'Aufgaben des gesetzlichen Betreuers - Zur Reform des Betreuungsrechts',
#             'Basisqualifikation für ungelernte Pflegekräfte (zertifiziert, berufsbegleitend)',
#             'Berufspädagogische Pflichtfortbildung für Praxisanleiter/-in (8 UE) - Online-Seminar',
#             'Berufspädagogische Pflichtfortbildung für Praxisanleiter/-innen (24 UE)',
#             'Berufspädagogische Pflichtfortbildung für Praxisanleiter/-innen (8 UE)',
#             'Beschäftigungs- und Aktivierungstherapie für dementiell erkrankte alte Menschen in stationären Altenhilfeeinrichtungen',
#             'Betreuungskraft gem. §§ 43b, 53c SGB XI (berufsbegleitend)',
#             'Demenz und Recht: Rechtssicheres Handeln zwischen Freiheit und Sicherheit',
#             'Dienstplangestaltung',
#             'Einführung in die Biografiearbeit mit alten Menschen',
#             'Entbürokratisierung in der Pflege - SIS verstehen und anwenden',
#             'Expertenstandard - Was gibt es Neues?',
#             'Fachkraft für gerontopsychiatrische Betreuung und Pflege (zertifiziert, berufsbegleitend)',
#             'Gerontopsychiatrische Grundlagen - Möglichkeiten personenzentrierter Kommunikation mit psychisch veränderten alten Menschen',
#             'Haftungsrecht in der Pflege',
#             'Humor für die Pflege (pflegen) - Online-Seminar',
#             'Hygienebeauftragte/-r in der Kita']
#         }


# Instantiate the app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# api = Api(app)

# # Create routes
# api.add_resource(Course, '/')
@app.route('/', methods=['GET'])
def api_get_users():
    return jsonify(get_courses())

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)