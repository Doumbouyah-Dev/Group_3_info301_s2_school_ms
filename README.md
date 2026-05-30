School Management System (Console-Based)

Overview

The School Management System is a Python-based console application designed to manage the daily operations of a school. It provides functionality for managing students, teachers, subjects, grades, enrollments, academic scores, and reports through an interactive menu-driven interface.

The system stores all data in JSON files, ensuring persistence between sessions without requiring a database.


---

Features

Student Management

Add new students

View all students

Update student information

Delete students

Search students by ID


Teacher Management

Add new teachers

View all teachers

Update teacher information

Delete teachers

Assign teachers to grades


Subject Management

Add subjects

View all subjects

Assign subjects to grades


Grade Management

Configure grades

View grades

Update grade descriptions

Delete grade configurations


Enrollment System

Enroll students into grades

View enrollment history


Score Management

Record student scores

View all scores

View scores by student

View scores by teacher


Reports & Summaries

Generate student report cards

List students by grade

Display total counts of students, teachers, subjects, and grades


Data Persistence

All records are automatically saved into JSON files:

students.json

teachers.json

subjects.json

grades.json

enrollments.json

scores.json



---

System Architecture

The application follows an object-oriented design consisting of the following major classes:

Student Class

Represents a student record.

Attributes

Attribute	Description

id	Student ID
name	Student name
grade	Current grade
dob	Date of birth
gender	Gender
phone	Phone number


Methods

to_list()

from_list()



---

Teacher Class

Represents a teacher.

Attributes

Attribute	Description

id	Teacher ID
name	Teacher name
qualification	Academic qualification
subjects	Subjects taught
phone	Contact number
assigned_grades	Grades assigned


Methods

to_list()

from_list()



---

Subject Class

Represents a school subject.

Attributes

Attribute	Description

id	Subject ID
name	Subject name
assigned_grades	Assigned grades


Methods

to_list()

from_list()



---

Grade Class

Represents a grade/class level.

Attributes

Attribute	Description

name	Grade name
description	Grade description


Methods

to_list()

from_list()



---

Enrollment Class

Tracks student enrollment history.

Attributes

Attribute	Description

student_id	Student identifier
grade_name	Grade enrolled in
enroll_date	Enrollment date


Methods

to_list()

from_list()



---

Score Class

Stores academic performance records.

Attributes

Attribute	Description

student_id	Student ID
subject_id	Subject ID
teacher_id	Teacher ID
score	Student score
date	Date recorded


Methods

to_list()

from_list()



---

Data Management

DataManager Class

Handles all file operations.

Responsibilities

Load data from JSON files

Save data to JSON files

Convert JSON records into objects

Convert objects into JSON-compatible lists


File Structure

FILES = {
    "students": "students.json",
    "teachers": "teachers.json",
    "subjects": "subjects.json",
    "grades": "grades.json",
    "enrollments": "enrollments.json",
    "scores": "scores.json"
}


---

Validation System

The application includes extensive validation to maintain data integrity.

Student ID Validation

Integers only

Prevents duplicate IDs


Name Validation

Allows:

A-Z
a-z
Spaces
Periods (.)
Apostrophes (')
Hyphens (-)

Examples:

John Doe
Mary-Jane
O'Connor


---

Date Validation

Required format:

YYYY-MM-DD

Example:

2005-08-15


---

Gender Validation

Accepted inputs:

M
Male
F
Female

Stored values:

Male
Female


---

Grade Validation

Available grades:

Grade 1
Grade 2
Grade 3
...
Grade 12


---

Phone Number Validation

Allowed prefixes:

0775
0776
0777
0778
0779
0770
0772
0760
0555
0886
0888
0880

Format:

Prefix + 6 digits

Example:

0777123456
0886123456


---

Main Menu Structure

1. Student Management
2. Teacher Management
3. Subject Management
4. Grade Management
5. Enrollment System
6. Score Management
7. Reports and Summaries
8. Save and Exit


---

Module Breakdown

Student Management Menu

1. Add Student
2. View All Students
3. Update Student
4. Delete Student
5. Search Student by ID
6. Back to Main Menu

Functionalities

Add Student

Creates a new student record.

View Students

Displays all registered students.

Update Student

Modifies existing student information.

Delete Student

Removes student and associated records.

Deletes:

Student record

Enrollment records

Score records


Search Student

Searches by student ID.


---

Teacher Management Menu

1. Add Teacher
2. View All Teachers
3. Assign Teacher to Grade
4. Update Teacher
5. Delete Teacher
6. Back

Functionalities

Assign Teacher to Grade

Allows teachers to be assigned to one or more grades.

Example:

Teacher A
 ├── Grade 7
 ├── Grade 8
 └── Grade 9


---

Subject Management Menu

1. Add Subject
2. View Subjects
3. Assign Subject to Grade
4. Back

Functionalities

Assign Subject to Grade

Example:

Mathematics
 ├── Grade 5
 ├── Grade 6
 └── Grade 7


---

Grade Management Menu

1. Add Grade
2. View Grades
3. Update Grade
4. Delete Grade
5. Back

Functionalities

Deleting a grade:

Removes grade configuration

Removes teacher assignments

Removes subject assignments

Removes enrollment records linked to that grade



---

Enrollment Menu

1. Enroll Student into Grade
2. View Enrollment History
3. Back

Functionalities

Enroll Student

Creates enrollment record.

Example:

Student ID: 1001
Grade: Grade 8
Date: 2025-01-15

Enrollment History

Displays all grade enrollments for a student.


---

Score Management Menu

1. Add Score
2. View All Scores
3. View Scores for Student
4. View Scores for Teacher
5. Back

Functionalities

Add Score

Requirements:

Valid student

Valid subject

Optional teacher


Score range:

0 - 100

View Scores

Displays:

Student name

Subject

Score

Teacher

Date



---

Reports and Summaries

Students by Grade

Displays all students enrolled in a selected grade.

Example:

Grade 8

ID: 101
John Doe

ID: 102
Mary Smith


---

Student Report Card

Example:

===== Report Card =====

Student: John Doe
Grade: Grade 8

Mathematics: 89
English: 92
Science: 84

=======================


---

Total Counts

Displays:

Total Students
Total Teachers
Total Subjects
Total Grades


---

Program Workflow

Start Program
      │
      ▼
Load JSON Data
      │
      ▼
Display Main Menu
      │
      ├── Student Management
      ├── Teacher Management
      ├── Subject Management
      ├── Grade Management
      ├── Enrollment System
      ├── Score Management
      └── Reports
      │
      ▼
Save Data
      │
      ▼
Exit


---

Installation

Prerequisites

Python 3.8+

No external libraries required



---

Clone or Download
git clone https://github.com/Doumbouyah-Dev/Group_3_info301_s2_school_ms.git
cd school-management-system

Or simply download:

schools_m.py


---

Running the Program

python schools_m.py


---

Sample Project Directory

SchoolManagementSystem/
│
├── schools_m.py
├── students.json
├── teachers.json
├── subjects.json
├── grades.json
├── enrollments.json
├── scores.json
└── README.md


---

Strengths of the System

✅ Object-Oriented Design

✅ JSON-Based Data Persistence

✅ Strong Input Validation

✅ Modular Architecture

✅ Enrollment Tracking

✅ Score Management

✅ Teacher-Grade Assignment

✅ Subject-Grade Assignment

✅ Report Card Generation

✅ Simple Console Interface

✅ No External Dependencies


---

Limitations

No graphical user interface (GUI)

No authentication/login system

No database integration

No attendance management

No fee/payment management

No automatic GPA calculation

No export to PDF/Excel

No student promotion system

No timetable management



---

Future Enhancements

User authentication and role management

Database support (MySQL/PostgreSQL)

GUI version using Tkinter or PyQt

Web-based version using Flask or Django

Attendance tracking

Fee management system

Automatic report card generation

Student promotion between grades

Performance analytics dashboard

Export reports to PDF and Excel

SMS/Email notifications



---

Author

School Management System Console-Based Academic Management Application

Developed in Python using Object-Oriented Programming principles and JSON data storage.


---
