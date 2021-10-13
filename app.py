try:
    from flask import Flask, render_template, url_for
    from flask_assets import Environment, Bundle
    import os
    import json

    with open("static/list_of_exercises.json", 'r') as file:
        EXERCISES = json.load(file)["exercises"]
    print("The imports were successful")
except:
    print("There was a problem with the imports!")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/select_exercise")
def select_exercise():
    return render_template("select_exercise.html",exercises=EXERCISES)

@app.route("/<exercise>")
def exercise(exercise):
    return render_template("exercise.html", exercise=exercise)

@app.route("/<exercise>/register_set")
def register_set(exercise):
    return render_template("register_set.html", exercise=exercise)

if(__name__ == "__main__"):
    app.run(debug=True)
    app.send_file_max_age_default = 0