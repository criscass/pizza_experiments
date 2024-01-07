import os
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField, TextAreaField, PasswordField, BooleanField
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
  flour_amount = IntegerField("gr.", validators=[DataRequired()])
  water_amount = IntegerField("water", validators=[DataRequired()])
  yeast_type = StringField("Type of yeast")
  yeast_amount = DecimalField("yeast gr.")
  salt_amount = DecimalField("salt")
  sugar_amount = DecimalField("sugar")
  oil_amount = DecimalField("oil")
  temperature = DecimalField("Temperature ℃")
  maturation_time = DecimalField("Maturation Time")
  procedure = TextAreaField("Procedure")
  result_vote = IntegerField("Result Vote")
  result_comment = TextAreaField("Result comment")
  submit = SubmitField("Submit")

#Create a login form
  class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


#              ______    _______  __   __  _______  _______  _______ 
#             |    _ |  |       ||  | |  ||       ||       ||       |
#             |   | ||  |   _   ||  | |  ||_     _||    ___||  _____|
#             |   |_||_ |  | |  ||  |_|  |  |   |  |   |___ | |_____ 
#             |    __  ||  |_|  ||       |  |   |  |    ___||_____  |
#             |   |  | ||       ||       |  |   |  |   |___  _____| |
#             |___|  |_||_______||_______|  |___|  |_______||_______|

  


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
  
  form = AddExperimentForm()

  if form.validate_on_submit():
      # Create a new Experiment instance with data from the form
      new_experiment = Experiment(
          flour_type=form.flour_type.data,
          flour_amount=form.flour_amount.data,
          water_amount=form.water_amount.data,
          yeast_type=form.yeast_type.data,
          yeast_amount=form.yeast_amount.data,
          salt_amount=form.salt_amount.data,
          sugar_amount=form.sugar_amount.data,
          oil_amount=form.oil_amount.data,
          temperature=form.temperature.data,
          maturation_time=form.maturation_time.data,
          procedure=form.procedure.data,
          result_vote=form.result_vote.data,
          result_comment=form.result_comment.data,
          user_id = 1  # Update with the actual user ID when you implement user authentication
      )

      # Add the new experiment to the database
      db.session.add(new_experiment)
      db.session.commit()

      return redirect(url_for('index'))  # Redirect to the home page after successful form submission

  return render_template("add_experiment.html", form=form)



