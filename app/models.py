from .extensions import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)
    double_auth_enabled = db.Column(db.Boolean, default=False)
    certified = db.Column(db.Boolean, default=False)
    anynonymous = db.Column(db.Boolean, default=False)
    dark_mode = db.Column(db.Boolean, default=False)
    news_letter_subscribed = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), default='user')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
