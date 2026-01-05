from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)

# Configure the database URI. Using SQLite file-based DB here
basedir = os.path.abspath(os.path.dirname(__file__))
print("The base dir is ", basedir)
db_name = "tasks.db"

final_db_path = os.path.join(basedir, db_name)

print("The final database path is ", final_db_path)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + final_db_path


db = SQLAlchemy(app) # Gives an object of type: Database -> This means that it will create a physical database file (.db file) and will give access to that file within app.py as an Object file

class Task(db.Model):
    __tablename__ = "tasks"                               # tablename explicitly names the table in the database
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id column in Task table
    title = db.Column(db.String(200), nullable=False)                 # title column in Task table
    completed = db.Column(db.Boolean, default=False)                  # completed column in Task table

with app.app_context():
    print("Creating database tables if they do not exist...")
    db.create_all()                                             # Creates tables (and generates a .db file) based on the type of database (which is SQLite here) by looking at app.config which is set to the joined strings (sqlite:/// + final_db_path)


@app.route('/')
def home():
    tasks = Task.query.all()                                 # The way you query all records from a table
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")                    # 'task' is the name attribute of the input field in index.html
    new_task = Task(title=task)                      # Create a new Task object
    db.session.add(new_task)                         # Add the new Task object to the session
    db.session.commit()                             # Commit the session to save the new task to the database
    return redirect("/")                            # Redirect back to the home page

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)          # Get the task by its ID    
    db.session.delete(task)                         # Delete the task from the session
    db.session.commit()                             # Commit the session to save changes to the database
    return redirect("/")                             # Redirect back to the home page

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if request.method == "POST":
        task.title = request.form.get("task")
        db.session.commit()
        return redirect("/")
    return render_template("edit.html", task=task)

if __name__ == "__main__": # "main" is the namespace
    app.run(debug=True)    # this namespace in addition to the run() method are both necessary for the app to run properly