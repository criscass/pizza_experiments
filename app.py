import os
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import json


app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

#Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///experiments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize the database
db = SQLAlchemy(app)

#The following line needs to run when creating the database
# app.app_context().push()


# Form secret key
# TODO: Change this in production and hide it in a env variable
app.config['SECRET_KEY'] = "V1hpvPBvka3GlrQ/61Sukg=="

# Create the experiments table (all amounts are in grams)
class Experiment(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
   flour_type = db.Column(db.String(50), nullable=False)
   flour_amount = db.Column(db.Integer, nullable=False)
   water_amount = db.Column(db.Integer, nullable=False)
   yeast_type = db.Column(db.String(50))
   yeast_amount = db.Column(db.Float)
   salt_amount = db.Column(db.Float)
   sugar_amount = db.Column(db.Float)
   oil_amount = db.Column(db.Float)
   temperature = db.Column(db.Float)
   maturation_time = db.Column(db.Float)
   procedure = db.Column(db.String(1000))
   result_vote = db.Column(db.Integer)
   result_comment = db.Column(db.String(500))
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create the users table
   class User(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(50), nullable=False)
      password = db.Column(db.String(100), nullable=False)

      experiments = db.relationship('Experiment', backref='user')
   
# Create a Form Class
class AddExperimentForm(FlaskForm):
  flour_type = StringField("Type of flour", validators=[DataRequired()])
  submit = SubmitField("Submit")

# # json file as temporary database
# def db():
#     filename = os.path.join(app.static_folder, 'db.json')
#     with open(filename) as db:
#         data = json.load(db)
#         return data

#home - home - home - home - home - home - home - home - home - home 
#home - home - home - home - home - home - home - home - home - home 
@app.route("/")
def index():
  # data=db()
  # i = 2
  return render_template("index.html")

#add-experiment - add-experiment - add-experiment - add-experiment
#add-experiment - add-experiment - add-experiment - add-experiment
@app.route("/add-experiment", methods=['GET','POST'])
def addExperiment():
  name = None
  form = AddExperimentForm()
  # validate form
  if form.validate_on_submit():
    name = form.name.data
    form.name.data = ""
  return render_template("add_experiment.html", name=name, form=form)
 


