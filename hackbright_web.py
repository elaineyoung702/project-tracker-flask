"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()


@app.route("/")
def get_homepage():
    """Display homepage"""

    STUDENT_QUERY = """
        SELECT first_name, last_name, github
        FROM students
        """

    student_db_cursor = db.session.execute(STUDENT_QUERY)

    student_rows = student_db_cursor.fetchall()

    PROJECT_QUERY = """
        SELECT title
        FROM projects
        """

    project_db_cursor = db.session.execute(PROJECT_QUERY)

    project_rows = project_db_cursor.fetchall()

    return render_template("homepage.html", student_rows=student_rows,
                            project_rows=project_rows)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    grades = hackbright.get_grades_by_github(github)

    return render_template('student_info.html', github=github, first=first, 
                            last=last, grades=grades)


@app.route("/student_search")
def get_student_form():
    """Show form for searching for a student"""

    return render_template("student_search.html")


@app.route("/student_add", methods=['GET'])
def student_add():
    """Add student to database."""

    return render_template("student_add.html")


@app.route("/student_conf", methods=['POST'])
def show_conf_page():
    """Show page confirming new student added."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)
    # first_name, last_name, github = hackbright.make_new_student(first_name, last_name, github)

    return render_template("student_conf.html", first_name=first_name, 
                           last_name=last_name, github=github)

@app.route("/project")
def show_project():
    """Show all details for project"""

    title = request.args.get("title")

    title, description, max_grade = hackbright.get_project_by_title(title)

    grades = hackbright.get_grades_by_title(title)

    return render_template("project.html", title=title, description=description, 
                            max_grade=max_grade, grades=grades) 


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
