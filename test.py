import json

with open("static/list_of_exercises.json", 'r') as file:
    exercises = json.load(file)["exercises"]
    print(exercises)
