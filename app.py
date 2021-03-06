# This is a program for gym guys
from flask import Flask, render_template, url_for, request
from datetime import date

from random import randint

from werkzeug.utils import redirect

from data_handler import Data_handler
from new_workout import New_workout

data = Data_handler()

new_workout = New_workout(str(date.today()))

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        data.save_to_file()

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

@app.route("/overview/<exercise>/<index>", methods=["POST", "GET"])
def exercise(exercise, index):
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

        pb = data.find_personal_best(exercise)
        reps = request.form.get("reps")
        weight = int(request.form.get("weight"))
        
        if pb == None:
            data.new_personal_best(exercise, weight)
        elif weight > int(pb):
            data.new_personal_best(exercise, weight)


        reps_weight = f"{weight}x{reps}"

        new_workout.add(data.exercise_to_index(exercise), reps_weight)


        return redirect(url_for("exercise", exercise=exercise, index=randint(0, 100)))

    return render_template("register_set.html", 
            exercise=exercise
        )

if(__name__ == "__main__"):
    app.run(debug=True)
    app.send_file_max_age_default = 0
