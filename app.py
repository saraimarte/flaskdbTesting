from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


db = SQLAlchemy()
app = Flask(__name__)
db_name = 'database.db'
app.config['SECRET_KEY'] = 'secretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class User(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw = {'placeholder':'Username'})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder':'Password'}
        )
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username = username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )
        

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw = {'placeholder':'Username'})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder':'Password'}
        )
    submit = SubmitField("Login")


db.init_app(app)


@app.route("/")

def home():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return render_template('home.html')
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form = form)

@app.route("/register",  methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', form = form)





if __name__ == '__main__':
    app.run(debug=True)












'''
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import sqlite3

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'helloworld'


class User(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(80), nullable = False)


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug = True)

    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)
'''