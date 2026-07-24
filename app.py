from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from database import create_table

app = Flask(__name__)
app.secret_key = "hostel123"

create_table()


def get_connection():
    conn = sqlite3.connect("hostel.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def do_login():

    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "admin":

        session["user"] = username

        return redirect("/dashboard")

    return "Invalid Username or Password"


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    conn = get_connection()

    total = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]

    conn.close()

    return render_template("dashboard.html", total=total)


@app.route("/add")
def add():

    if "user" not in session:
        return redirect("/")

    return render_template("add_student.html")


@app.route("/insert", methods=["POST"])
def insert():

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO students
        (name,age,gender,room,phone,course,fee_status)

        VALUES(?,?,?,?,?,?,?)
        """,
        (
            request.form["name"],
            request.form["age"],
            request.form["gender"],
            request.form["room"],
            request.form["phone"],
            request.form["course"],
            request.form["fee"],
        ),
    )

    conn.commit()
    conn.close()

    return redirect("/students")


@app.route("/students")
def students():

    conn = get_connection()

    data = conn.execute("SELECT * FROM students").fetchall()

    conn.close()

    return render_template("students.html", students=data)


@app.route("/delete/<int:id>")
def delete(id):

    conn = get_connection()

    conn.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()

    conn.close()

    return redirect("/students")


@app.route("/edit/<int:id>")
def edit(id):

    conn = get_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id=?", (id,)
    ).fetchone()

    conn.close()

    return render_template("edit_student.html", student=student)


@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    conn = get_connection()

    conn.execute(
        """
        UPDATE students

        SET

        name=?,
        age=?,
        gender=?,
        room=?,
        phone=?,
        course=?,
        fee_status=?

        WHERE id=?
        """,
        (
            request.form["name"],
            request.form["age"],
            request.form["gender"],
            request.form["room"],
            request.form["phone"],
            request.form["course"],
            request.form["fee"],
            id,
        ),
    )

    conn.commit()

    conn.close()

    return redirect("/students")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


create_table()

app = app

if __name__ == "__main__":
    app.run(debug=True)