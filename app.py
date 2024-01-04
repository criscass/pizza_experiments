from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/add-experiment")
def addExperiment():
  return render_template("add_experiment.html")
 

