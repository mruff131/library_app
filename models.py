from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets



login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()  #built in sql

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique= True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify   #if user opts to for google authenicator verification
    
    def set_token(self, length):
        return (secrets.token_hex(length))

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'User {self.email} has been added to the database.'
    

class Library(db.Model):
    id = db.Column(db.String, primary_key=True)
    book_type = db.Column(db.String(12))
    author_first = db.Column(db.String(150), nullable=False)
    author_last = db.Column(db.String(150))
    title = db.Column(db.String(150))   
    book_len = db.Column(db.Integer)
    isbn = db.Column(db.Integer)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, book_type, author_first, author_last, title, book_len, isbn, user_token, id= ''):
        self.id = self.set_id()
        self.author_first = author_first
        self.author_last = author_last
        self.title = title
        self.book_len = book_len 
        self.book_type = book_type
        self.user_token = user_token
        self.isbn = isbn

    def __repr__(self):
        return f'The following car has been added to the application.'
    
    def set_id(self):
        return (str(uuid.uuid4()))
    
        
class LibrarySchema(ma.Schema):
    class Meta:
        fields = ['id', 'book_type', 'author_first', 'author_last', 'title', 'book_len', 'isbn']

class UserSchema(ma.Schema):
    class Meta:
        fields = ['id', 'first_name', 'last_name', 'password', 'email' ]   #this info makes info from class serialized and  puts in json format and displays to user
        
lib_schema = LibrarySchema()
libs_schema = LibrarySchema(many=True)

user_schema = UserSchema()