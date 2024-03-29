from product_app import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import DataRequired, InputRequired, EqualTo
from sqlalchemy import Enum
from werkzeug.security import check_password_hash, generate_password_hash

import enum

class RolUser(enum.Enum):
    regular='regular'
    admin='admin'

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(255))
    pwhash=db.Column(db.String(255))
    rol=db.Column(Enum(RolUser))
    #products=db.relationship('Product', backref='category', lazy='select')
    
    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)
    
    def __init__(self, username, pwhash, rol=RolUser.regular):
        self.username=username
        self.pwhash=generate_password_hash(pwhash)
        self.rol=rol
        
    def __repr__(self):
        return '[User %r]' % (self.username)

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)
    
class LoginForm(FlaskForm):
    username=StringField('Nombre', validators=[DataRequired()])
    password=PasswordField('Contrasena', validators=[DataRequired()])
    next=HiddenField('next')
    
class RegisterForm(FlaskForm):
    username=StringField('Nombre', validators=[DataRequired()])
    password=PasswordField('Contrasena', validators=[DataRequired(),EqualTo('confirm')])
    confirm  = PasswordField('Repetir contrasena')
    
class ChangePassword(FlaskForm):
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords deben coincidir')])
    confirm  = PasswordField('Repeat Password')
    
    
    