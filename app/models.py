from .extensions import db, login_manager
from flask_login import UserMixin

# =======================
#        USER
# =======================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    phone_number = db.Column(db.String(20), unique=True, nullable=True)

    double_auth_enabled = db.Column(db.Boolean, default=False)
    certified = db.Column(db.Boolean, default=False)
    anonymous = db.Column(db.Boolean, default=False)
    dark_mode = db.Column(db.Boolean, default=False)
    news_letter_subscribed = db.Column(db.Boolean, default=True)

    role = db.Column(db.String(20), default='user')

    # relation : un user → plusieurs comptes bancaires
    bank_accounts = db.relationship('MainBankAccount', backref='user', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =======================
#   MAIN BANK ACCOUNT
# =======================

class MainBankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_origin = db.Column(db.String(256), nullable=False)
    account_name = db.Column(db.String(256), unique=True, nullable=False)
    type_account = db.Column(db.String(256), nullable=False)
    monnaie = db.Column(db.String(10), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    iban = db.Column(db.String(24), unique=True, nullable=False)
    status = db.Column(db.Boolean, default=False)
    main_account = db.Column(db.Boolean, default=False)

    # Relation avec User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship : compte -> transactions
    transactions = db.relationship('Transaction', backref='account', lazy=True)

# =======================
#      TRANSACTION
# =======================

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    account_label = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    category = db.Column(db.String(256), nullable=True)
    amount = db.Column(db.Float, nullable=False, default=0.0)

    # Relation vers le compte bancaire
    account_id = db.Column(db.Integer, db.ForeignKey('main_bank_account.id'), nullable=False)

    # Relation vers l'utilisateur (utile pour retrouver toutes ses transactions)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
