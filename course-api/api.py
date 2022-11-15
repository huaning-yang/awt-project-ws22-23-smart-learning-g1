# CourseOverview Service

# Import framework
from flask import Flask
from flask_restful import Resource, Api
import json
from dataclasses import dataclass
from dataclass_wizard import fromlist

@dataclass
class Course(Resource):
    # course_id: str
    # course_name: str

    # def __init__(self, course_id, course_name):
    #     self.course_id = id
    #     self.course_name = course_name

    # def __str__(self):
    #     return "({0}) {1}".format(self.course_id, self.course_name)

    # def get(self):
    #     # Opening JSON file
    #     f = open('/usr/src/app/courses.json')

    #     # returns JSON object as 
    #     # a dictionary
    #     jsonData = json.load(f)
    #     # courses = Course(**jsonData)
    #     courses = fromlist(Course, jsonData)
    #     print(courses[0])
    #     # Closing file
    #     f.close()
    #     return courses

    def get(self):
        return {
            'Courses': ['Aktuelles Arbeitsrecht 2022', 'Ambulante Pflege - Rechtssicher Handeln und Haftungsrisiken vermeiden', 
            'Aufgaben des gesetzlichen Betreuers - Zur Reform des Betreuungsrechts',
            'Basisqualifikation für ungelernte Pflegekräfte (zertifiziert, berufsbegleitend)',
            'Berufspädagogische Pflichtfortbildung für Praxisanleiter/-in (8 UE) - Online-Seminar',
            'Berufspädagogische Pflichtfortbildung für Praxisanleiter/-innen (24 UE)',
            'Berufspädagogische Pflichtfortbildung für Praxisanleiter/-innen (8 UE)',
            'Beschäftigungs- und Aktivierungstherapie für dementiell erkrankte alte Menschen in stationären Altenhilfeeinrichtungen',
            'Betreuungskraft gem. §§ 43b, 53c SGB XI (berufsbegleitend)',
            'Demenz und Recht: Rechtssicheres Handeln zwischen Freiheit und Sicherheit',
            'Dienstplangestaltung',
            'Einführung in die Biografiearbeit mit alten Menschen',
            'Entbürokratisierung in der Pflege - SIS verstehen und anwenden',
            'Expertenstandard - Was gibt es Neues?',
            'Fachkraft für gerontopsychiatrische Betreuung und Pflege (zertifiziert, berufsbegleitend)',
            'Gerontopsychiatrische Grundlagen - Möglichkeiten personenzentrierter Kommunikation mit psychisch veränderten alten Menschen',
            'Haftungsrecht in der Pflege',
            'Humor für die Pflege (pflegen) - Online-Seminar',
            'Hygienebeauftragte/-r in der Kita']
        }

    # @classmethod
    # def from_dict(cls, dict):
    #     return cls(course_id=dict["course_id"], course_name=dict["course_name"])

    # @classmethod
    # def from_json(cls, json_str: str):
    #     return cls.from_dict(json.loads(json_str))

# Instantiate the app
app = Flask(__name__)
api = Api(app)

# Create routes
api.add_resource(Course, '/')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)