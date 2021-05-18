try:
    from flask import Flask, render_template, url_for
    from flask_assets import Environment, Bundle
    import os
    import json
    print("The imports were successful")
except:
    print("There was a problem with the imports!")

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1> This is the start of something! <h1>"