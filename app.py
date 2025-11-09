"""
app.py
Simple PostgreSQL CRUD app for the `students` table.

Implements:
- getAllStudents(): list all students
- addStudent(): insert a new student (with validation)
- updateStudentEmail(): update email by student_id
- deleteStudent(): delete by student_id
- Text menu to call each function
"""

import psycopg2
from psycopg2 import errors
from datetime import datetime

# ----------------- Database Configuration -----------------
# Make sure to change password to whatever your password is (I keep forgetting).
DB_CONFIG = {
    "dbname": "students_db",
    "user": "postgres",
    "password": "yourpasswordhere",
    "host": "localhost",
    "port": "5432",
}


def connect_db():
    """
    Create and return a new PostgreSQL connection using DB_CONFIG.

    Returns:
        psycopg2 connection object

    Raises:
        psycopg2.Error if connection fails.
    """
    return psycopg2.connect(**DB_CONFIG)


# ----------------- CRUD Functions -----------------

def getAllStudents():
    """
    Retrieve and print all students from the 'students' table.

    Behavior:
        - Executes:
            SELECT student_id, first_name, last_name, email, enrollment_date
            FROM students
            ORDER BY student_id;
        - Prints each record to the console.
        - On error, prints a message and returns to menu.
    """
    try:
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT student_id, first_name, last_name, email, enrollment_date
                    FROM students
                    ORDER BY student_id;
                    """
                )
                rows = cur.fetchall()

                if not rows:
                    print("\nNo students found.\n")
                    return

                print("\nAll Students:")
                print("ID | First Name | Last Name | Email | Enrollment Date")
                print("-" * 70)
                for sid, first, last, email, enroll_date in rows:
                    print(f"{sid} | {first} | {last} | {email} | {enroll_date}")
                print()
    except psycopg2.Error as e:
        print(f"\n[ERROR] Failed to fetch students: {e.pgerror or e}\n")


def addStudent(first, last, email, date_str):
    """
    Insert a new student into the 'students' table.

    Args:
        first (str): First name
        last  (str): Last name
        email (str): Unique email
        date_str (str): Enrollment date in 'YYYY-MM-DD' format

    Behavior:
        - Validates date format before sending to DB.
        - On success, prints new student_id.
        - On error, prints a friendly message and returns to menu.
    """
    # Validate date format
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("\n[ERROR] Invalid date format. Use YYYY-MM-DD (e.g., 2023-09-01).\n")
        return

    try:
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO students (first_name, last_name, email, enrollment_date)
                    VALUES (%s, %s, %s, %s)
                    RETURNING student_id;
                    """,
                    (first, last, email, date_str),
                )
                new_id = cur.fetchone()[0]
                conn.commit()
                print(f"\nStudent added with ID {new_id}.\n")

    except errors.UniqueViolation:
        # Email must be unique
        print("\n[ERROR] That email is already in use. Please use a different email.\n")
    except psycopg2.Error as e:
        print(f"\n[ERROR] Failed to add student: {e.pgerror or e}\n")


def updateStudentEmail(student_id, new_email):
    """
    Update a student's email.

    Args:
        student_id (str or int): ID of the student to update
        new_email (str): New email address

    Behavior:
        - Converts student_id to int.
        - Executes UPDATE on the matching row.
        - Prints result.
    """
    try:
        sid = int(student_id)
    except ValueError:
        print("\n[ERROR] Invalid student ID. Please enter a number.\n")
        return

    try:
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE students
                    SET email = %s
                    WHERE student_id = %s;
                    """,
                    (new_email, sid),
                )

                if cur.rowcount == 0:
                    print("\nNo student found with that ID.\n")
                else:
                    conn.commit()
                    print("\nEmail updated successfully.\n")

    except errors.UniqueViolation:
        print("\n[ERROR] That email is already in use. Please use a different email.\n")
    except psycopg2.Error as e:
        print(f"\n[ERROR] Failed to update email: {e.pgerror or e}\n")


def deleteStudent(student_id):
    """
    Delete a student by ID.

    Args:
        student_id (str or int): ID of the student to delete

    Behavior:
        - Converts student_id to int.
        - Executes DELETE on matching row.
        - Prints result.
    """
    try:
        sid = int(student_id)
    except ValueError:
        print("\n[ERROR] Invalid student ID. Please enter a number.\n")
        return

    try:
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM students WHERE student_id = %s;",
                    (sid,),
                )

                if cur.rowcount == 0:
                    print("\nNo student found with that ID.\n")
                else:
                    conn.commit()
                    print("\nStudent deleted successfully.\n")

    except psycopg2.Error as e:
        print(f"\n[ERROR] Failed to delete student: {e.pgerror or e}\n")


# ----------------- Menu / Entry Point -----------------

def menu():
    """
    Simple interactive menu loop for calling CRUD operations.
    """
    while True:
        print("--- Students CRUD Menu ---")
        print("1. View all students")
        print("2. Add a student")
        print("3. Update student email")
        print("4. Delete a student")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            getAllStudents()
        elif choice == "2":
            first = input("First name: ").strip()
            last = input("Last name: ").strip()
            email = input("Email: ").strip()
            date = input("Enrollment date (YYYY-MM-DD): ").strip()
            addStudent(first, last, email, date)
        elif choice == "3":
            sid = input("Student ID: ").strip()
            new_email = input("New email: ").strip()
            updateStudentEmail(sid, new_email)
        elif choice == "4":
            sid = input("Student ID to delete: ").strip()
            deleteStudent(sid)
        elif choice == "0":
            print("\nGoodbye.")
            break
        else:
            print("\nInvalid option. Please try again.\n")


if __name__ == "__main__":
    # On start, verifuy that we can connect with the given config
    try:
        with connect_db() as _:
            pass
    except psycopg2.Error as e:
        print(f"[ERROR] Could not connect to database with current DB_CONFIG:\n{e.pgerror or e}")
    else:
        menu()
