"""
Latest Edit: August 15, 2020

Team Kalinaw Website Main Program for Impact Hackathon

Install:
 - pip install flask, SQLAlchemy, flask_bootstrap, flask_wtf, flask-sqlalchemy, flask_login, email_validator

requirements.txt
 - pip freeze > requirements.txt

"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

#Import libraries
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


#--------------------------------------------------------------------------------------------------------------------------------------------
app = Flask(__name__) # Start of Flask App
bootstrap = Bootstrap(app) # For WTForms
app.config['SECRET_KEY'] = 'temporarykey123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Ignore Warning message
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3' # db Will show up in this directory
#app.config['SQLALCHEMY_DATABASE_URI'] = postgresql://scott:tiger@localhost/mydatabase
db = SQLAlchemy(app) # Initialize SQLAlchemy app

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Class that represents user database ==========================================================================================================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    date_created = db.Column(db.DateTime, default=datetime.now)
    option = db.Column(db.String(20))
    profession = db.Column(db.String(50))
    residence = db.Column(db.String(100))
    organization = db.Column(db.String(50))
    essay = db.Column(db.String(200))

class Yield(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50))
    year = db.Column(db.Integer)
    regioncar = db.Column(db.Float)
    regionone = db.Column(db.Float)
    regiontwo = db.Column(db.Float)
    regionthr = db.Column(db.Float)
    regionfoa = db.Column(db.Float)
    regionfob = db.Column(db.Float)
    regionfiv = db.Column(db.Float)
    regionsix = db.Column(db.Float)
    regionsev = db.Column(db.Float)
    regioneig = db.Column(db.Float)
    regionnin = db.Column(db.Float)
    regionten = db.Column(db.Float)
    regionele = db.Column(db.Float)
    regiontwe = db.Column(db.Float)
    regionthn = db.Column(db.Float)
    regionarm = db.Column(db.Float)

class Volume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(50))
    year = db.Column(db.Integer)
    regioncar = db.Column(db.Float)
    regionone = db.Column(db.Float)
    regiontwo = db.Column(db.Float)
    regionthr = db.Column(db.Float)
    regionfoa = db.Column(db.Float)
    regionfob = db.Column(db.Float)
    regionfiv = db.Column(db.Float)
    regionsix = db.Column(db.Float)
    regionsev = db.Column(db.Float)
    regioneig = db.Column(db.Float)
    regionnin = db.Column(db.Float)
    regionten = db.Column(db.Float)
    regionele = db.Column(db.Float)
    regiontwe = db.Column(db.Float)
    regionthn = db.Column(db.Float)
    regionarm = db.Column(db.Float)


"""
Initialize in Terminal with Python to make the User db above

>>> from main import db
>>> db.create_all()

"""

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Enter Username', validators=[InputRequired(), Length(min=4, max=80)])
    password = PasswordField('Enter Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=30)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=4, max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=4, max=30)])
    age = StringField('Age', validators=[InputRequired(), Length(min=1, max=10)])

    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80),
                                                    EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

    option = SelectField('Farmer, Educator, or Intern?', choices = [('Farmer', 'Farmer'), ('Educator', 'Educator'), ('Intern', 'Intern')], validators = [InputRequired()])

    profession = StringField('Profession', validators=[InputRequired(), Length(min=4, max=30)])
    residence = StringField('City', validators=[InputRequired(), Length(min=1, max=50)])
    organization = StringField('Organization', validators=[InputRequired(),Length(min=4, max=30)])
    essay = StringField('Why do you want to be a Farmer, Educator or Intern?', validators=[InputRequired(), Length(min=4, max=200)])

# Connecting to www.website.com/home
@app.route("/home")
@app.route('/')
def index():
    #user = db.session.query(User.username)
    return render_template('home.html')

@app.route("/soon")
def soon():
    return render_template('soon.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_password,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        age=form.age.data,
                        option=form.option.data,
                        profession=form.profession.data,
                        residence=form.residence.data,
                        organization=form.organization.data,
                        essay=form.essay.data,
                        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)



@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    import random
    number1 = random.randint(1000,500000)
    number2 = random.randint(1000,500000)
    number3 = random.randint(1000,500000)
    line = "static/charts/dasline.png?" + str(number1)
    bar = "static/charts/dasbar.png?" + str(number2)
    price_chart = "static/charts/price.png?" + str(number3)

    if request.method == 'POST':
        try:
            area = pd.read_csv('data/Yield.csv')
            crop = request.form['crops']
            region = request.form['region']
            crop_val =  area[area.Crop==crop]
            fig = plt.figure(figsize=(8,4)) #inches
            axes = fig.add_axes([0,0,1,1])
            axes.set_title(crop+ ' Production Yield for '+ region)
            axes.plot(crop_val['Year'], crop_val[region])
            axes.set_xlabel('Year', fontsize=10)
            axes.set_ylabel("mTon/Hectares", fontsize=10)
            axes.grid(True)
            fig.savefig("static/charts/dasline.png", bbox_inches='tight')

            new = crop_val.append(crop_val.sum(numeric_only=True), ignore_index=True)
            new['Crop'] = new['Crop'].fillna('total')
            total = new[new['Crop'] == 'total']
            total_data= total.drop(['Year', 'Crop'],axis=1)
            ax = total_data.plot(kind='bar', width=1,figsize=(10,8),
                         title='Total '+ crop+ ' Produce | 2014 - 2018')
            fig1 = ax.get_figure()
            fig1.savefig("static/charts/dasbar.png")

            price = pd.read_csv('data/palay_price.csv')
            fig2 = plt.figure(figsize=(8,4)) #inches
            ax2 = fig2.add_axes([0,0,1,1])
            ax2.set_title('Palay Price in php/kg')
            ax2.plot(price['Year'], price[region])
            ax2.set_xlabel('Year', fontsize=10)
            ax2.set_ylabel("Price in php/kg", fontsize=10)
            ax2.grid(True)
            fig2.savefig("static/charts/price.png", bbox_inches='tight')
            plt.tight_layout
        except:
            redirect(url_for('dashboard'))

    return render_template('dashboard.html', name=current_user.first_name, random=random, line=line, bar=bar, price_chart=price_chart)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ====================================================================================================================================================================
@app.route("/regioni", methods=['GET','POST'])
def regioni():
    import random
    number1 = random.randint(1000,500000)
    number2 = random.randint(1000,500000)
    line = "static/charts/iline.png?" + str(number1)
    bar = "static/charts/ibar.png?" + str(number2)

    if request.method == 'POST':
        try:
            area = pd.read_csv('data/Yield.csv')
            crop = request.form['crops']
            region = request.form['region']
            crop_val =  area[area.Crop==crop]
            fig = plt.figure(figsize=(8,4)) #inches
            axes = fig.add_axes([0,0,1,1])
            axes.set_title(crop+ ' Production Yield for '+ region)
            axes.plot(crop_val['Year'], crop_val[region])
            axes.set_xlabel('Year', fontsize=10)
            axes.set_ylabel("mTon/Hectares", fontsize=10)
            axes.grid(True)
            fig.savefig("static/charts/iline.png", bbox_inches='tight')

            new = crop_val.append(crop_val.sum(numeric_only=True), ignore_index=True)
            new['Crop'] = new['Crop'].fillna('total')
            total = new[new['Crop'] == 'total']
            total_data= total.drop(['Year', 'Crop'],axis=1)
            ax = total_data.plot(kind='bar', width=1,figsize=(10,8),
                         title='Total '+ crop+ ' Produce | 2014 - 2018')
            fig1 = ax.get_figure()
            fig1.savefig("static/charts/ibar.png")
        except:
            redirect(url_for('regioni'))

    return render_template("regions/regioni.html", random=random, line=line,bar=bar)


@app.route("/regionii", methods=['GET','POST'])
def regionii():
    import random
    number1 = random.randint(1000,500000)
    number2 = random.randint(1000,500000)
    line = "static/charts/iiline.png?" + str(number1)
    bar = "static/charts/iibar.png?" + str(number2)

    if request.method == 'POST':
        try:
            area = pd.read_csv('data/Yield.csv')
            crop = request.form['crops']
            region = request.form['region']
            crop_val =  area[area.Crop==crop]
            fig = plt.figure(figsize=(8,4)) #inches
            axes = fig.add_axes([0,0,1,1])
            axes.set_title(crop+ ' Production Yield for '+ region)
            axes.plot(crop_val['Year'], crop_val[region])
            axes.set_xlabel('Year', fontsize=10)
            axes.set_ylabel("mTon/Hectares", fontsize=10)
            axes.grid(True)
            fig.savefig("static/charts/iiline.png", bbox_inches='tight')

            new = crop_val.append(crop_val.sum(numeric_only=True), ignore_index=True)
            new['Crop'] = new['Crop'].fillna('total')
            total = new[new['Crop'] == 'total']
            total_data= total.drop(['Year', 'Crop'],axis=1)
            ax = total_data.plot(kind='bar', width=1,figsize=(10,8),
                         title='Total '+ crop+ ' Produce | 2014 - 2018')
            fig1 = ax.get_figure()
            fig1.savefig("static/charts/iibar.png")
        except:
            redirect(url_for('regionii'))

    return render_template("regions/regionii.html", random=random, line=line,bar=bar)


@app.route("/regioniii", methods=['GET','POST'])
def regioniii():
    import random
    number1 = random.randint(1000,500000)
    number2 = random.randint(1000,500000)
    line = "static/charts/iiiline.png?" + str(number1)
    bar = "static/charts/iiibar.png?" + str(number2)

    if request.method == 'POST':
        try:
            area = pd.read_csv('data/Yield.csv')
            crop = request.form['crops']
            region = request.form['region']
            crop_val =  area[area.Crop==crop]
            fig = plt.figure(figsize=(8,4)) #inches
            axes = fig.add_axes([0,0,1,1])
            axes.set_title(crop+ ' Production Yield for '+ region)
            axes.plot(crop_val['Year'], crop_val[region])
            axes.set_xlabel('Year', fontsize=10)
            axes.set_ylabel("mTon/Hectares", fontsize=10)
            axes.grid(True)
            fig.savefig("static/charts/iiiline.png", bbox_inches='tight')

            new = crop_val.append(crop_val.sum(numeric_only=True), ignore_index=True)
            new['Crop'] = new['Crop'].fillna('total')
            total = new[new['Crop'] == 'total']
            total_data= total.drop(['Year', 'Crop'],axis=1)
            ax = total_data.plot(kind='bar', width=1,figsize=(10,8),
                         title='Total '+ crop+ ' Produce | 2014 - 2018')
            fig1 = ax.get_figure()
            fig1.savefig("static/charts/iiibar.png")
        except:
            redirect(url_for('regioniii'))

    return render_template("regions/regioniii.html", random=random, line=line,bar=bar)


@app.route("/regioniva", methods=['GET','POST'])
def regioniva():
    import random
    number1 = random.randint(1000,500000)
    number2 = random.randint(1000,500000)
    line = "static/charts/ivaline.png?" + str(number1)
    bar = "static/charts/ivabar.png?" + str(number2)

    if request.method == 'POST':
        try:
            area = pd.read_csv('data/Yield.csv')
            crop = request.form['crops']
            region = request.form['region']
            crop_val =  area[area.Crop==crop]
            fig = plt.figure(figsize=(8,4)) #inches
            axes = fig.add_axes([0,0,1,1])
            axes.set_title(crop+ ' Production Yield for '+ region)
            axes.plot(crop_val['Year'], crop_val[region])
            axes.set_xlabel('Year', fontsize=10)
            axes.set_ylabel("mTon/Hectares", fontsize=10)
            axes.grid(True)
            fig.savefig("static/charts/ivaline.png", bbox_inches='tight')

            new = crop_val.append(crop_val.sum(numeric_only=True), ignore_index=True)
            new['Crop'] = new['Crop'].fillna('total')
            total = new[new['Crop'] == 'total']
            total_data= total.drop(['Year', 'Crop'],axis=1)
            ax = total_data.plot(kind='bar', width=1,figsize=(10,8),
                         title='Total '+ crop+ ' Produce | 2014 - 2018')
            fig1 = ax.get_figure()
            fig1.savefig("static/charts/ivabar.png")
        except:
            redirect(url_for('regioniva'))

    return render_template("regions/regioniva.html", random=random, line=line,bar=bar)



@app.route("/regionivb", methods=['GET','POST'])
def regionivb():
    import random
    number1 = random.randint(1000,500000)
    number2 = random.randint(1000,500000)
    line = "static/charts/ivbline.png?" + str(number1)
    bar = "static/charts/ivbbar.png?" + str(number2)

    if request.method == 'POST':
        try:
            area = pd.read_csv('data/Yield.csv')
            crop = request.form['crops']
            region = request.form['region']
            crop_val =  area[area.Crop==crop]
            fig = plt.figure(figsize=(8,4)) #inches
            axes = fig.add_axes([0,0,1,1])
            axes.set_title(crop+ ' Production Yield for '+ region)
            axes.plot(crop_val['Year'], crop_val[region])
            axes.set_xlabel('Year', fontsize=10)
            axes.set_ylabel("mTon/Hectares", fontsize=10)
            axes.grid(True)
            fig.savefig("static/charts/ivbline.png", bbox_inches='tight')

            new = crop_val.append(crop_val.sum(numeric_only=True), ignore_index=True)
            new['Crop'] = new['Crop'].fillna('total')
            total = new[new['Crop'] == 'total']
            total_data= total.drop(['Year', 'Crop'],axis=1)
            ax = total_data.plot(kind='bar', width=1,figsize=(10,8),
                         title='Total '+ crop+ ' Produce | 2014 - 2018')
            fig1 = ax.get_figure()
            fig1.savefig("static/charts/ivbbar.png")
        except:
            redirect(url_for('regionivb'))

    return render_template("regions/regionivb.html", random=random, line=line,bar=bar)
    #return render_template("regions/car.html", region=region)



@app.route("/car", methods=['GET','POST'])
def car():
    """
    CAR Page
    """
    import random
    number1 = random.randint(1000,500000)
    number2 = random.randint(1000,500000)
    line = "static/charts/carline.png?" + str(number1)
    bar = "static/charts/carbar.png?" + str(number2)

    if request.method == 'POST':
        try:
            area = pd.read_csv('data/Yield.csv')
            crop = request.form['crops']
            region = request.form['region']
            crop_val =  area[area.Crop==crop]
            fig = plt.figure(figsize=(8,4)) #inches
            axes = fig.add_axes([0,0,1,1])
            axes.set_title(crop+ ' Production Yield for '+ region)
            axes.plot(crop_val['Year'], crop_val[region])
            axes.set_xlabel('Year', fontsize=10)
            axes.set_ylabel("mTon/Hectares", fontsize=10)
            axes.grid(True)
            fig.savefig("static/charts/carline.png", bbox_inches='tight')

            new = crop_val.append(crop_val.sum(numeric_only=True), ignore_index=True)
            new['Crop'] = new['Crop'].fillna('total')
            total = new[new['Crop'] == 'total']
            total_data= total.drop(['Year', 'Crop'],axis=1)
            ax = total_data.plot(kind='bar', width=1,figsize=(10,8),
                         title='Total '+ crop+ ' Produce | 2014 - 2018')
            fig1 = ax.get_figure()
            fig1.savefig("static/charts/carbar.png")
        except:
            redirect(url_for('car'))

    return render_template("regions/car.html", random=random, line=line,bar=bar)
    #return render_template("regions/car.html", region=region)

# ================================================================================================================================================================================================

#---------------------------------------------------------------------------------------------------------------------------------------------
# End of Flask App
if __name__ == "__main__":
#    app.run(host='0.0.0.0')
   app.run(debug=True)
