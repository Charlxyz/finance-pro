from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user
from ..models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    return render_template("auth/login.html")

@auth_bp.route("/register")
def register():
    return render_template("auth/register.html")

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))