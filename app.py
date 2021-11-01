from flask import Flask, render_template, url_for, request
from flask_assets import Environment, Bundle
import os
from datetime import date

from werkzeug.utils import redirect

from data_handler import Data_handler
from new_workout import New_workout

data = Data_handler()

new_workout = New_workout(str(date.today()))

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/select_exercise", methods=["POST", "GET"])
def select_exercise():
    if request.method == "POST":
        print("This is the active workout!", new_workout.into_dict())

        data.add(new_workout)
        new_workout.clear()

        return redirect(url_for("home"))
        

    return render_template("select_exercise.html",
            exercises=data.get_list_of_exercises()
        )

@app.route("/overview/<exercise>", methods=["POST", "GET"])
def exercise(exercise):
    active_workout = new_workout.current_exercise(data.exercise_to_index(exercise))

    if request.method == "POST":
        print("This is the active workout!", active_workout)
        

    date, sets = data.find_prev_workout(exercise)
    pb = data.find_personal_best(exercise)

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

        reps = request.form.get("reps")
        weight = request.form.get("weight")
        
        reps_weight = f"{weight}x{reps}"

        new_workout.add(data.exercise_to_index(exercise), reps_weight)


        return redirect(url_for("exercise", exercise=exercise))

    return render_template("register_set.html", 
            exercise=exercise
        )

if(__name__ == "__main__"):
    app.run(debug=True)
    app.send_file_max_age_default = 0