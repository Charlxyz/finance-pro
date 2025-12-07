from flask import Blueprint, redirect, render_template, request, flash
from flask_login import logout_user

# Création du blueprint
main_bp = Blueprint("main", __name__)

# Route d'accueil
@main_bp.route("/")
def home():
    return render_template("home.html")

# Exemple : page "à propos"
@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@main_bp.route("/contact")
def contact():
    return render_template("contact.html")

@main_bp.route("/invest")
def invest():
    return render_template("invest.html")

@main_bp.route("/analyses")
def analyses():
    return render_template("analyses.html")

@main_bp.route("/account")
def account():
    flash("Bienvenue sur votre page de compte !", "success")
    flash("N'oubliez pas de vérifier vos informations.", "info")
    flash("Erreur lors du chargement des données.", "error")
    flash("Ceci est un avertissement.", "warning")
    
    user = {
        "name": "Jean Dupont",
        "email": "jean.dupont@example.com",
        "active": True,
        "initials": "JD"
    }

    balances = {
        "total": "12 450 €",
        "income": "2 300 €",
        "expense": "1 260 €"
    }

    return render_template("account.html", user=user, balances=balances)

@main_bp.route("/account/edit", methods=["GET", "POST"])
def edit_account():

    # Simulation d'un utilisateur existant
    user = {
        "name": "Jean Dupont",
        "email": "jean.dupont@example.com",
        "initials": "JD",
        "darkmode": True,
        "newsletter": False
    }

    if request.method == "POST":

        # Récupération des informations
        name = request.form.get("name")
        email = request.form.get("email")
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        darkmode = "darkmode" in request.form
        newsletter = "newsletter" in request.form

        # Photo de profil
        avatar_file = request.files.get("avatar")
        if avatar_file:
            print("Nouvelle photo uploadée :", avatar_file.filename)

        # Vérification du mot de passe
        if new_password and new_password != confirm_password:
            return "Les mots de passe ne correspondent pas"

        print("MODIFICATIONS ENREGISTRÉES :")
        print(name, email, darkmode, newsletter)

        # Redirection
        return redirect("/account")

    return render_template("edit_account.html", user=user)
