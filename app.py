import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError,EqualTo, Optional, Email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt






app = Flask(__name__)

if __name__ == "__main__":
  app.run(port=8000, debug=True)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///experiments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=365) #change remember me time
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)
app.config['REMEMBER_COOKIE_SECURE'] = False


#Initialize the database
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
# Form secret key
# TODO: Change this in production and hide it in a env variable
app.config['SECRET_KEY'] = "V1hpvPBvka3GlrQ/61Sukg=="

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))
  

# Database - Database - Database - Database - Database - Database - Database
# Database - Database - Database - Database - Database - Database - Database

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
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(25), nullable=False, unique=True)
  email = db.Column(db.String(30), nullable=False, unique=True)
  password = db.Column(db.String(100), nullable=False)

  experiments = db.relationship('Experiment', backref='user')


 # Forms - Forms - Forms - Forms - Forms - Forms - Forms - Forms - Forms - Forms
 # Forms - Forms - Forms - Forms - Forms - Forms - Forms - Forms - Forms - Forms
   
# Create a Form Class
class AddExperimentForm(FlaskForm):
  flour_type = StringField("Type of flour", validators=[InputRequired()])
  flour_amount = IntegerField("grams", validators=[InputRequired()])
  water_amount = IntegerField("water", validators=[InputRequired()])
  yeast_type = StringField("Type of yeast", validators=[Optional()])
  yeast_amount = DecimalField("grams", validators=[Optional()])
  salt_amount = DecimalField("salt", validators=[Optional()])
  sugar_amount = DecimalField("sugar", validators=[Optional()])
  oil_amount = DecimalField("oil", validators=[Optional()])
  temperature = DecimalField("Temperature ℃", validators=[Optional()])
  maturation_time = DecimalField("Maturation (hours)", validators=[Optional()])
  procedure = TextAreaField("Procedure", validators=[Optional()])
  result_vote = IntegerField("Vote", validators=[Optional()])
  result_comment = TextAreaField("Result comment", validators=[Optional()])
  submit = SubmitField("Submit")

#Create a login form
class LoginForm(FlaskForm):
  email = StringField('Email', validators=[Email(message='You need to input a valid email')])
  password = PasswordField('Password', validators=[DataRequired(),InputRequired(),Length(min=8,max=20)])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Login')

  def validate_email(self, email):
    existing_email = User.query.filter_by(email=email.data).first()
    
    if not existing_email:
      raise ValidationError("This email hasn't been registered")
  

#Create a registration form
class RegisterForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(),InputRequired(),Length(min=4,max=20)])
  email = StringField('Email', validators=[DataRequired(), Email(message='You need to input a valid email')])
  password = PasswordField('Password', validators=[DataRequired(),Length(min=8,max=20)])
  confirm  = PasswordField('Repeat Password', validators=[DataRequired(),EqualTo('password', message='Passwords must match')])
  submit = SubmitField('Register')

  def validate_email(self, email):
    existing_email = User.query.filter_by(email=email.data).first()
    
    if existing_email:
      raise ValidationError("This email has already been used.")
    
  def validate_username(self, username):
    existing_username = User.query.filter_by(username=username.data).first()
    
    if existing_username:
      raise ValidationError("This username already exists, please choose another one.")  


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
@login_required
def index():
  experiments = Experiment.query.filter_by(user_id = current_user.id)
  return render_template("index.html", experiments=experiments)

# calculator - calculator - calculator - calculator - calculator - calculator
# calculator - calculator - calculator - calculator - calculator - calculator
@app.route("/calculator", methods=['GET'])
@login_required
def calculator():
  
  return render_template("calculator.html")

#login - login - login - login - login - login - login - login - login
#login - login - login - login - login - login - login - login - login
@app.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for("index"))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user:
      if bcrypt.check_password_hash(user.password, form.password.data):

        login_user(user, remember=form.remember_me.data)
        flash('Logged in successfully.')
        return redirect(url_for("index"))
  return render_template("login.html", form=form)



#logout - logout - logout - logout - logout - logout - logout - logout - logout
#logout - logout - logout - logout - logout - logout - logout - logout - logout
@app.route("/logout", methods=['GET','POST'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))


#register - register - register - register - register - register - register
#register - register - register - register - register - register - register
@app.route("/register", methods=['GET','POST'])
def register():
  form = RegisterForm()

  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data)
    new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, remember_me=form.remember_me.data)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))
  else:
    print(form.errors.items())
  
  return render_template("register.html", form=form)

#add-experiment - add-experiment - add-experiment - add-experiment
#add-experiment - add-experiment - add-experiment - add-experiment
@app.route("/add-experiment", methods=['GET','POST'])
@login_required
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
          user_id = current_user.id
      )
     
      # Add the new experiment to the database
      db.session.add(new_experiment)
      db.session.commit()

      return redirect(url_for('index'))  # Redirect to the home page after successful form submission

  return render_template("add_experiment.html", form=form)


@app.route("/experiment/<experiment_id>", methods=['GET'])
@login_required
def experiment(experiment_id):
  experiment = Experiment.query.filter_by(id = experiment_id)
  return render_template("experiment.html", exp=experiment)


