from flask import Flask, render_template, url_for
from flask_assets import Environment, Bundle
from data_handler import Data_handler
import os

data = Data_handler()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/select_exercise")
def select_exercise():
    return render_template("select_exercise.html",
            exercises=data.get_list_of_exercises()
        )

@app.route("/<exercise>")
def exercise(exercise):
    date, sets = data.find_prev_workout(exercise)
    pb = data.find_personal_best(exercise)
    return render_template("exercise.html", 
            exercise = exercise, 
            date = date,
            sets = sets,
            pb=pb
        )

@app.route("/<exercise>/register_set")
def register_set(exercise):
    return render_template("register_set.html", 
            exercise=exercise
        )

if(__name__ == "__main__"):
    app.run(debug=True)
    app.send_file_max_age_default = 0