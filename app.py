import os
from flask import Flask, render_template, redirect, url_for, flash
from markupsafe import Markup
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError,EqualTo, Optional, Email
from flask_sqlalchemy import SQLAlchemy, session
from datetime import datetime, timedelta
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from dotenv import load_dotenv
import urllib.parse as up
import psycopg2






app = Flask(__name__)



load_dotenv()

#Change in production
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=365) #change remember me time
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)
app.config['REMEMBER_COOKIE_SECURE'] = False



#Initialize the database
up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)

bcrypt = Bcrypt(app)
# Form secret key
# TODO: Change this in production and hide it in a env variable
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))
  
db = SQLAlchemy(app)

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
   yeast_amount = db.Column(db.Integer)
   salt_amount = db.Column(db.Integer)
   sugar_amount = db.Column(db.Integer)
   oil_amount = db.Column(db.Integer)
   temperature = db.Column(db.Float)
   maturation_time = db.Column(db.Float)
   procedure = db.Column(db.String(3000))
   result_vote = db.Column(db.Float)
   result_comment = db.Column(db.String(1000))
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create the users table
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(30), nullable=False, unique=True)
  email = db.Column(db.String(30), nullable=False, unique=True)
  password = db.Column(db.LargeBinary(80), nullable=False)

  experiments = db.relationship('Experiment', backref='user')


 # Forms - Forms - Forms - Forms - Forms - Forms - Forms - Forms - Forms - Forms
 # Forms - Forms - Forms - Forms - Forms - Forms - Forms - Forms - Forms - Forms
   
# Create a Form Class
class AddExperimentForm(FlaskForm):
  flour_type = StringField("Type of flour", validators=[InputRequired()])
  flour_amount = IntegerField("grams", validators=[InputRequired()])
  water_amount = IntegerField("water", validators=[InputRequired()])
  yeast_type = StringField("Type of yeast", validators=[Optional()])
  yeast_amount = IntegerField("grams", validators=[Optional()])
  salt_amount = IntegerField("salt", validators=[Optional()])
  sugar_amount = IntegerField("sugar", validators=[Optional()])
  oil_amount = IntegerField("oil", validators=[Optional()])
  temperature = DecimalField("Temperature ℃", validators=[Optional()])
  maturation_time = DecimalField("Maturation (hours)", validators=[Optional()])
  label_for_procedure = Markup('Procedure <span class="small-label">(max 3000 characters)</span>')
  procedure = TextAreaField(label_for_procedure, validators=[Optional(), Length(max=3000)])
  result_vote = DecimalField("Vote", validators=[Optional()])
  result_comment = TextAreaField("Result comment (max 1000 characters)", validators=[Optional(), Length(max=1000)])
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

# delete - delete - delete - delete - delete - delete - delete - delete - delete - delete - delete - delete
# delete - delete - delete - delete - delete - delete - delete - delete - delete - delete - delete - delete
@app.route("/delete/<int:id>", methods=['GET','POST'])
@login_required
def delete(id):
  experiment_to_delete = Experiment.query.filter_by(id=id).first()
  try:
    db.session.delete(experiment_to_delete)
    db.session.commit()
    experiments = Experiment.query.filter_by(user_id = current_user.id)
    return render_template("index.html", experiments=experiments)
  except:
    return "There was a problem deleting this experiment"
  

# Edit experiment - Edit experiment - Edit experiment - Edit experiment - Edit experiment - Edit experiment
# Edit experiment - Edit experiment - Edit experiment - Edit experiment - Edit experiment - Edit experiment
@app.route("/experiment/edit/<int:id>", methods=['GET','POST'])
@login_required
def edit_experiment(id):
  experiment = Experiment.query.filter_by(id=id).first()
  form = AddExperimentForm()
  if form.validate_on_submit():
      experiment.flour_type=form.flour_type.data
      experiment.flour_amount=form.flour_amount.data
      experiment.water_amount=form.water_amount.data
      experiment.yeast_type=form.yeast_type.data
      experiment.yeast_amount=form.yeast_amount.data
      experiment.salt_amount=form.salt_amount.data
      experiment.sugar_amount=form.sugar_amount.data
      experiment.oil_amount=form.oil_amount.data
      experiment.temperature=form.temperature.data
      experiment.maturation_time=form.maturation_time.data
      experiment.procedure=form.procedure.data
      experiment.result_vote=form.result_vote.data
      experiment.result_comment=form.result_comment.data
      #update database
      db.session.add(experiment)
      db.session.commit()
      flash("Experiment has been updated")
      return redirect(url_for("experiment", id=id))
  form.flour_type.data = experiment.flour_type
  form.flour_amount.data = experiment.flour_amount
  form.water_amount.data = experiment.water_amount
  form.yeast_type.data = experiment.yeast_type
  form.yeast_amount.data = experiment.yeast_amount
  form.salt_amount.data = experiment.salt_amount
  form.sugar_amount.data = experiment.sugar_amount
  form.oil_amount.data = experiment.oil_amount
  form.temperature.data = experiment.temperature
  form.maturation_time.data = experiment.maturation_time
  form.procedure.data = experiment.procedure
  form.result_vote.data = experiment.result_vote
  form.result_comment.data = experiment.result_comment
  return render_template('edit_experiment.html', form=form, id=experiment.id)

#login - login - login - login - login - login - login - login - login
#login - login - login - login - login - login - login - login - login
@app.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for("index"))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data.lower()).first()
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
    new_user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_password)
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

# Experiment - Experiment - Experiment - Experiment - Experiment - Experiment - Experiment - Experiment
# Experiment - Experiment - Experiment - Experiment - Experiment - Experiment - Experiment - Experiment
@app.route("/experiment/<int:id>", methods=['GET'])
@login_required
def experiment(id):
  experiment = Experiment.query.filter_by(id = id).first()
  return render_template("experiment.html", exp=experiment)

if __name__ == "__main__":
  app.run()


