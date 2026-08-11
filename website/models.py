from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    date = db.Column(db.DateTime(timezone=True), default=datetime.now)
    debit = db.Column(db.Integer)
    credit = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    category = db.Column(db.String(1000))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(10000))
    first_name = db.Column(db.String(150))
    categories = db.Column(db.String(100000), default="General")
    budgets = db.Column(db.String(100000), default="1000")
    expenses = db.relationship('Expense')
