from datetime import datetime
from flaskr import db
# from flask_login import UserMixin

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# create a table
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    profile_image = db.Column(db.String(100), nullable=False, default='my_profile.png')
    email = db.Column(db.String(100), unique=True, nullable=False)
    # we hash the user password to a 60 string long
    password = db.Column(db.String(60), nullable=False)
    job_title = db.Column(db.String(60))
    interests = db.Column(db.Text)
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'))
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    # education_level_id = db.Column(db.Integer, db.ForeignKey('education_level.id'))
    # relationships
    events = db.relationship('Event', backref='author', lazy=True)
    # campus = db.relationship("Campus", back_populates="campuses")
    # major = db.relationship("Major", back_populates="majors")
    # group = db.relationship("Group", back_populates="groups")
    # educational_level = db.relationship("EducationLevel", back_populates="education_levels")


class Group(db.Model):
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship("User", backref="group")


# class EducationLevel(db.Model):
#     __tablename__ = "education_level"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     users = db.relationship("User", backref="education_level")


class Campus(db.Model):
    __tablename__ = "campus"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    majors = db.relationship('Major', backref='author', lazy=True)
    users = db.relationship("User", backref="campus")


class Major(db.Model):
    __tablename__ = "major"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'), nullable=False) 
    users = db.relationship("User", backref="major")


class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



"""
Implement Chat
https://www.youtube.com/watch?v=uJC8A_7VZOA&ab_channel=IndianPythonista

from flaskr import db, app
from flaskr.model import Group, Campus, Major
---
alu = Campus(name='ALU')
alc = Campus(name='ALC')
db.session.add(alu)
db.session.add(alc)
db.session.commit()
------
cs = Major(name='Global Challenges', author=alu)
gc = Major(name='Global Challenges', author=alu)
en = Major(name="entrepreneurship", author=alu)
ib = Major(name="international business and trade", author=alu)
db.session.add(cs)
db.session.add(gc)
db.session.add(en)
db.session.add(ib)
db.session.commit()
----
s = Group(name='Student')
a = Group(name='Alumni')
f = Group(name="Facilitator")
o = Group(name="Other Staff")
db.session.add(a)
db.session.add(s)
db.session.add(f)
db.session.add(o)
db.session.commit()
----
"""