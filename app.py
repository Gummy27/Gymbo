from flask import Flask, render_template, url_for, request, session, redirect
from flask_session import Session

import os

from datetime import date

from random import randint

from data_handler import Data_handler
from new_workout import New_workout

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SESSION_COOKIE_NAME"] = "my_session"

Session(app)

@app.before_first_request
def intitialize_session():
    session["new_workout"] = New_workout(str(date.today()))
    session["data"] = Data_handler()


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        session["data"].save_to_file()

    return render_template("home.html")

@app.route("/select_exercise", methods=["POST", "GET"])
def select_exercise():
    if request.method == "POST":
        print("This is the active workout!", session["new_workout"].into_dict())

        session["data"].add(session["new_workout"])
        session["new_workout"].clear()

        return redirect(url_for("home"))
        

    return render_template("select_exercise.html",
            exercises=session["data"].get_list_of_exercises()
        )

@app.route("/overview/<exercise>/<index>", methods=["POST", "GET"])
def exercise(exercise, index):
    active_workout = session["new_workout"].current_exercise(session["data"].exercise_to_index(exercise))

    if request.method == "POST":
        print("This is the active workout!", active_workout)
        

    date, sets = session["data"].find_prev_workout(exercise)
    pb = session["data"].find_personal_best(exercise)

    print("This is new workout", active_workout)

    return render_template("exercise.html", 
            exercise = exercise, 
            date = date,
            sets = sets,
            pb=pb,
            active_workout=active_workout
        )

@app.route("/<exercise>/register_set", methods=["POST", "GET"])
def register_set(exercise):
    if request.method == "POST":

        pb = session["data"].find_personal_best(exercise)
        reps = request.form.get("reps")
        weight = int(request.form.get("weight"))
        
        if pb == None:
            session["data"].new_personal_best(exercise, weight)
        elif weight > int(pb):
            session["data"].new_personal_best(exercise, weight)


        reps_weight = f"{weight}x{reps}"

        session["new_workout"].add(session["data"].exercise_to_index(exercise), reps_weight)


        return redirect(url_for("exercise", exercise=exercise, index=randint(0, 100)))

    return render_template("register_set.html", 
            exercise=exercise
        )

@app.route("/json")
def json():
    return session["data"].get_json() 

if(__name__ == "__main__"):
    app.run(debug=True)
    app.send_file_max_age_default = 0