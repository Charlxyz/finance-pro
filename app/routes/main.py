from flask import Blueprint, redirect, render_template, request, flash
from flask_login import logout_user
from ..models import User
from ..extensions import db

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

@main_bp.route("/conditions")
def conditions():
    return render_template("user_condition.html")

@main_bp.route("/confidentialite")
def confidentiality():
    return render_template("confidentiality.html")

@main_bp.route("/faq")
def faq():
    return render_template("faq.html")

@main_bp.route("/invest")
def invest():
    return render_template("invest.html")

@main_bp.route("/analyses")
def analyses():
    return render_template("analyses.html")

@main_bp.route("/account")
def account():
    user = User.query.first()

    balances = {
        "total": "12 450 €",
        "income": "2 300 €",
        "expense": "1 260 €"
    }

    return render_template("account.html", user=user, balances=balances)

@main_bp.route("/account/edit", methods=["GET", "POST"])
def edit_account():
    user = User.query.first()

    if request.method == "POST":
        print(request.form)

        # Récupération des informations
        name = request.form.get("name")
        email = request.form.get("email")
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        darkmode = "darkmode" in request.form
        newsletter = "newsletter" in request.form

        if name:
            user.name = name
        if email:
            user.email = email

        user.dark_mode = True if darkmode else False
        user.news_letter_subscribed = True if newsletter else False

        # Photo de profil
        avatar_file = request.files.get("avatar")
        if avatar_file:
            print("Nouvelle photo uploadée :", avatar_file.filename)

        # Vérification du mot de passe
        if new_password and new_password != confirm_password:
            flash("Les mots de passe ne correspondent pas", "error")

        if old_password and new_password:
            if user.check_password(old_password):
                user.set_password(new_password)
            else:
                flash("Ancien mot de passe incorrect", "error")

        db.session.commit()
        flash("Compte mis à jour avec succès", "success")
        return redirect("/account")

    return render_template("edit_account.html", user=user)

@main_bp.route("/bank-accounts")
def comptes_bancaires():
    # Simulation : ces données viendront plus tard de ta base SQL
    accounts = [
        {
            "id": 1,
            "bank_name": "BNP Paribas",
            "label": "Compte courant perso",
            "type": "Compte courant",
            "currency": "EUR",
            "iban_masked": "FR76 **** **** 1234 5678 901",
            "balance": "3 250 €",
            "balance_numeric": 3250,
            "active": True,
        },
        {
            "id": 2,
            "bank_name": "Crédit Agricole",
            "label": "Livret A",
            "type": "Épargne",
            "currency": "EUR",
            "iban_masked": "FR12 **** **** 9876 5432 109",
            "balance": "8 700 €",
            "balance_numeric": 8700,
            "active": True,
        },
        {
            "id": 3,
            "bank_name": "Boursorama",
            "label": "Compte joint",
            "type": "Compte courant",
            "currency": "EUR",
            "iban_masked": "FR98 **** **** 4567 8901 234",
            "balance": "13 480 €",
            "balance_numeric": 13480,
            "active": False,
        },
    ]

    summary = {
        "total_balance": "25 430 €",
        "count": len(accounts),
        "main_bank": "BNP Paribas",
    }

    transactions = [
        {
            "date": "08/12/2025",
            "account_label": "Compte courant perso",
            "description": "Paiement CB Supermarché",
            "category": "Courses",
            "amount": "- 84 €",
            "amount_numeric": -84,
        },
        {
            "date": "05/12/2025",
            "account_label": "Compte courant perso",
            "description": "Virement salaire",
            "category": "Revenu",
            "amount": "+ 2 300 €",
            "amount_numeric": 2300,
        },
        {
            "date": "03/12/2025",
            "account_label": "Livret A",
            "description": "Transfert vers épargne",
            "category": "Épargne",
            "amount": "+ 500 €",
            "amount_numeric": 500,
        },
        {
            "date": "01/12/2025",
            "account_label": "Compte joint",
            "description": "Loyer",
            "category": "Logement",
            "amount": "- 950 €",
            "amount_numeric": -950,
        },
    ]

    return render_template(
        "bank_accounts.html", accounts=accounts, summary=summary, transactions=transactions,)

@main_bp.route("/bank-accounts/<int:account_id>")
def compte_detail(account_id):

    # Exemple de comptes simulés (à remplacer par ta base SQL plus tard)
    accounts = {
        1: {
            "bank_name": "BNP Paribas",
            "label": "Compte courant perso",
            "type": "Compte courant",
            "currency": "EUR",
            "iban": "FR7612345678901234567890123",
            "balance": "3 250 €",
            "balance_numeric": 3250,
            "active": True,
        },
        2: {
            "bank_name": "Crédit Agricole",
            "label": "Livret A",
            "type": "Épargne",
            "currency": "EUR",
            "iban": "FR1298765432109876543210987",
            "balance": "8 700 €",
            "balance_numeric": 8700,
            "active": True,
        },
        3: {
            "bank_name": "Boursorama",
            "label": "Compte joint",
            "type": "Compte courant",
            "currency": "EUR",
            "iban": "FR9845678901234567890123456",
            "balance": "13 480 €",
            "balance_numeric": 13480,
            "active": False,
        }
    }

    # Récupère le compte correspondant à l'id
    account = accounts.get(account_id)

    if not account:
        return "Compte introuvable", 404

    # Transactions fictives (à filtrer plus tard par compte_id)
    transactions = [
        {"date": "05/12/2025", "description": "Salaire", "amount": "+ 2 300 €", "amount_numeric": 2300},
        {"date": "06/12/2025", "description": "Restaurant", "amount": "- 42 €", "amount_numeric": -42},
        {"date": "07/12/2025", "description": "Essence", "amount": "- 65 €", "amount_numeric": -65},
    ]

    return render_template("bank_accounts_detail.html", account=account, transactions=transactions)

@main_bp.route("/bank-accounts/<int:account_id>/operations")
def compte_operations(account_id):

    # Exemple de comptes simulés (plus tard → SQL)
    accounts = {
        1: "Compte courant perso",
        2: "Livret A",
        3: "Compte joint"
    }

    account_label = accounts.get(account_id)

    if not account_label:
        return "Compte introuvable", 404

    # Transactions fictives du compte sélectionné
    operations = [
        {"date": "08/12/2025", "category": "Courses", "desc": "Supermarché", "amount": "- 84 €", "amount_numeric": -84},
        {"date": "07/12/2025", "category": "Essence", "desc": "Station Total", "amount": "- 65 €", "amount_numeric": -65},
        {"date": "05/12/2025", "category": "Revenu", "desc": "Salaire", "amount": "+ 2 300 €", "amount_numeric": 2300},
        {"date": "03/12/2025", "category": "Épargne", "desc": "Virement Livret A", "amount": "+ 250 €", "amount_numeric": 250},
        {"date": "01/12/2025", "category": "Abonnement", "desc": "Netflix", "amount": "- 15 €", "amount_numeric": -15},
    ]

    # Résumé
    summary = {
        "total_ops": len(operations),
        "total_in": sum(op["amount_numeric"] for op in operations if op["amount_numeric"] > 0),
        "total_out": sum(op["amount_numeric"] for op in operations if op["amount_numeric"] < 0),
    }

    return render_template("bank_accounts_operation.html", account_id=account_id, account_label=account_label, operations=operations, summary=summary)
