from bs4 import BeautifulSoup
from dataclasses import dataclass
import sqlite3
from sqlite3 import Error

# Reading the data inside the xml
# file to a variable under the name
# data
with open('data\AWT_small.xml', 'r') as f:
    data = f.read()

# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object
Bs_data = BeautifulSoup(data, "xml")

# Finding all instances of tag
# `unique`
b_courses = Bs_data.find_all('COURSE')

b_coursesuppliers = Bs_data.find_all('COURSESUPPLIER')


@dataclass
class Course():
    CS_NAME: str
    CS_ID: str
    CS_LANGUAGE: str
    CS_SUPPLIERID: str
    CS_DEGREE_EXAM: int
    CS_PRICE: float
    CS_WDB_TYPE: int
    CS_WDB_MODE: int
    CS_WDB_UNTERRICHTSSTUNDEN_ANZAHL: int

    def __init__(self, NAME, ID, LANGUAGE, SUPPLIERID, DEGREE_EXAM, PRICE, WDB_TYPE, WDB_MODE, WDB_UNTERRICHTSSTUNDEN_ANZAHL):
        self.CS_ID = ID
        self.CS_NAME = NAME
        self.CS_LANGUAGE = LANGUAGE
        self.CS_SUPPLIERID = SUPPLIERID
        self.CS_DEGREE_EXAM = DEGREE_EXAM
        self.CS_PRICE = PRICE
        self.CS_WDB_TYPE = WDB_TYPE
        self.CS_WDB_MODE = WDB_MODE
        self.CS_WDB_UNTERRICHTSSTUNDEN_ANZAHL = WDB_UNTERRICHTSSTUNDEN_ANZAHL

    def __str__(self):
        return "({0}) {1}".format(self.CS_ID, self.CS_NAME)

    def getList(self):
        return [self.CS_ID, self.CS_NAME, self.CS_LANGUAGE, self.CS_SUPPLIERID,  self.CS_DEGREE_EXAM, self.CS_PRICE, self.CS_WDB_TYPE, self.CS_WDB_MODE, self.CS_WDB_UNTERRICHTSSTUNDEN_ANZAHL]

@dataclass
class CourseSupplier():
    CSS_NAME: str
    CSS_ID: str

    def __init__(self, name, id):
        self.CSS_NAME = id
        self.CSS_ID = name

    def __str__(self):
        return "({0}) {1}".format(self.CSS_ID, self.CSS_NAME)

    def getList(self):
        return [self.CSS_ID, self.CSS_NAME]


courses = []
coursesuppliers = []

for b_course in b_courses[:1]:
    course = Course(b_course.CS_NAME.text, b_course.CS_ID.text, b_course.CS_LANGUAGE.text, b_course.CS_SUPPLIERID.text, b_course.CS_DEGREE_EXAM.text, b_course.CS_PRICE.text, b_course.CS_WDB_TYPE.text, b_course.CS_WDB_MODE.text, b_course.CS_WDB_UNTERRICHTSSTUNDEN_ANZAHL.text)
    courses.append(course)

for b_coursesupplier in b_coursesuppliers[:1]:
    coursesupplier = CourseSupplier(
        b_coursesupplier.CSS_NAME.text, b_coursesupplier.CSS_ID.text)
    coursesuppliers.append(coursesupplier)

print(len(courses))
print(len(coursesuppliers))

# Sqlite insert
# taken from https://www.sqlitetutorial.net/sqlite-python/insert/
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_course(conn, course):
    """
    Create a new course into the courses table
    :param conn:
    :param course:
    """
    sql = ''' INSERT INTO courses(CS_NAME, CS_ID, CS_LANGUAGE, CS_SUPPLIERID, CS_DEGREE_EXAM, CS_PRICE, CS_WDB_TYPE, CS_WDB_MODE, CS_WDB_UNTERRICHTSSTUNDEN_ANZAHL) VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()

    cur.execute(sql, (course.CS_NAME, course.CS_ID, course.CS_LANGUAGE, course.CS_SUPPLIERID, course.CS_DEGREE_EXAM, course.CS_PRICE, course.CS_WDB_TYPE, course.CS_WDB_MODE, course.CS_WDB_UNTERRICHTSSTUNDEN_ANZAHL))
    conn.commit()

def create_coursesupplier(conn, coursesupplier):
    """
    Create a new coursesupplier into the coursesuppliers table
    :param conn:
    :param coursesupplier:
    """
    sql = ''' INSERT INTO coursesuppliers(CSS_NAME, CSS_ID) VALUES(?,?) '''
    cur = conn.cursor()

    cur.execute(sql, (coursesupplier.CSS_NAME, coursesupplier.CSS_ID))
    conn.commit()

def insert_courses(conn, courses):
    """
    Create a new course into the courses table
    :param conn:
    :param course:
    """
    sql = ''' INSERT INTO courses(CS_NAME, CS_ID, CS_LANGUAGE, CS_SUPPLIERID, CS_DEGREE_EXAM, CS_PRICE, CS_WDB_TYPE, CS_WDB_MODE, CS_WDB_UNTERRICHTSSTUNDEN_ANZAHL) VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()

    cur.executemany(sql, [course.getList() for course in courses])
    conn.commit()
    print(cur.rowcount, "Records inserted successfully into courses table")

def insert_coursesupplier(conn, coursesuppliers):
    """
    Create a new coursesupplier into the coursesuppliers table
    :param conn:
    :param coursesupplier:
    """
    sql = ''' INSERT INTO coursesuppliers(CSS_NAME, CSS_ID) VALUES(?,?) '''
    cur = conn.cursor()

    cur.executemany(sql, [coursesupplier.getList() for coursesupplier in coursesuppliers])
    conn.commit()
    print(cur.rowcount, "Records inserted successfully into coursesuppliers table")

database = r"data\database.db"

# create a database connection
conn = create_connection(database)
with conn:
    cur = conn.cursor()
    with open('data\db\courses.sql','r', encoding='utf-8') as f:
        cur.executescript(f.read())
    with open('data\db\coursesupplier.sql','r', encoding='utf-8') as f:
        cur.executescript(f.read())
    cur.executescript('DELETE FROM courses')
    cur.executescript('DELETE FROM coursesuppliers')
    conn.commit()
    # for course in courses:
    #     course_id = create_course(conn, course)
    insert_courses(conn, courses)
    insert_coursesupplier(conn, coursesuppliers)
