from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import environment, mode
from typing import Callable

env = environment[0] if mode == 'development' else environment[1]

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{env.USER}:{env.PASS}@{env.HOST}:{env.PORT}/{env.DB}'


class PSQLAlchemy(SQLAlchemy):
    Column: Callable
    Integer: Callable
    String: Callable
    DateTime: Callable


db = PSQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    username = db.Column(db.String, unique = True, nullable = False)
    server = db.Column(db.String, nullable = False)
    last_activity = db.Column(db.String)
    last_activity_loc = db.Column(db.String)
    last_activity_ts = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User(id = {self.id}, username = {self.username}, last_activity = {self.last_activity},' \
               f' last_activity_loc = {self.last_activity_loc}, last_activity_ts = {self.last_activity_ts})>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Server(db.Model):
    __tablename__ = 'servers'

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    server = db.Column(db.String, nullable = False)
    last_activity = db.Column(db.String)
    last_activity_ts = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User(id = {self.id}, server = {self.server}, last_activity = {self.last_activity},' \
               f' last_activity_ts = {self.last_activity_ts})>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
