PostgreSQL CRUD Application (Python)
------------------------------------

Description:

A simple Python application that connects to a PostgreSQL database and performs
Create, Read, Update, and Delete (CRUD) operations on a "students" table.

------------------------------------
SETUP INSTRUCTIONS
------------------------------------

1. Create the database in pgAdmin or in the psql shell, run:
       CREATE DATABASE students_db;

2. Run the provided schema.sql file inside the students_db database.


3. Open app.py and update the password field in DB_CONFIG with yourPostgreSQL password:

   "password": "yourpasswordhere"

------------------------------------
REQUIREMENTS
------------------------------------

- PostgreSQL installed and running
- Python 3.x
- psycopg2-binary package

Install the required Python package:
   
    pip install psycopg2-binary

------------------------------------
RUNNING THE APPLICATION
------------------------------------

From your project folder, run:
    py app.py

You will see a menu like this:

    --- Students CRUD Menu ---
    1. View all students
    2. Add a student
    3. Update student email
    4. Delete a student
    0. Exit

Choose an option and follow the prompts.

------------------------------------
AUTHOR
------------------------------------

- Name: Ahmad Kanaan
- Student Number: 101276072
- Course: COMP 3005 – Database Management Systems
- Date: November 2025
