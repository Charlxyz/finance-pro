from datetime import datetime
from flask import Blueprint, redirect, render_template, request, flash
from flask_login import current_user, login_required, logout_user
from ..models import User, MainBankAccount, Transaction
from ..extensions import db

# Création du blueprint
main_bp = Blueprint("main", __name__)

# Route d'accueil
@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@main_bp.route("/invest")
def invest():
    return render_template("invest.html")

@main_bp.route("/analyses")
def analyses():
    return render_template("analyses.html")

# --- Dossier INFO ---
@main_bp.route("/contact")
def contact():
    return render_template("info/contact.html")

@main_bp.route("/faq")
def faq():
    return render_template("info/faq.html")

# --- Dossier LEGAL ---

@main_bp.route("/conditions")
def conditions():
    return render_template("legal/user_condition.html")

@main_bp.route("/confidentialite")
def confidentiality():
    return render_template("legal/confidentiality.html")

# --- Dossier account ---
@main_bp.route("/account")
def account():
    user = User.query.first()

    balances = {
        "total": "12 450 €",
        "income": "2 300 €",
        "expense": "1 260 €"
    }

    return render_template("account/account.html", user=user, balances=balances)

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

    return render_template("account/edit_account.html", user=user)

# --- Dossier bank ---
@main_bp.route("/bank-accounts")
def comptes_bancaires():
    accounts = MainBankAccount.query.all()
    transac = Transaction.query.all()
    
    summary = {
        "total_balance": f"{sum(acc.balance for acc in accounts)} {accounts[0].monnaie if accounts else '€'}",
        "count": len(accounts),
        "main_bank": "BNP Paribas" if accounts else "N/A",
    }

    transactions = [
        {
            "date": t.date,
            "account_label": t.account_label,
            "description": t.description,
            "category": t.category,
            "amount": f"{t.amount} €",
            "amount_numeric": t.amount,   # nombre, pas une liste
        }
        for t in transac
    ]

    return render_template(
        "bank/bank_accounts.html", accounts=accounts, summary=summary, transactions=transactions,)

@main_bp.route("/bank-accounts/<int:account_id>")
def compte_detail(account_id):
    accounts_query = MainBankAccount.query.all()
    transactions = Transaction.query.filter_by(account_id=account_id).all()

    accounts = {
        acc.id: {
            "id": acc.id,
            "bank_name": acc.bank_origin,
            "label": acc.account_name,
            "type": acc.type_account,
            "currency": acc.monnaie,
            "iban": acc.iban,
            "balance": f"{acc.balance} {acc.monnaie}",
            "balance_numeric": acc.balance,
            "active": acc.status,
        }
        for acc in accounts_query
    } 

    # Récupère le compte correspondant à l'id
    account = accounts.get(account_id)

    if not account:
        flash("Compte introuvable", "error")
        return redirect("/bank-accounts")

    return render_template("bank/bank_accounts_detail.html", account=account, transactions=transactions)

@main_bp.route("/bank-accounts/<int:account_id>/operations")
def compte_operations(account_id):
    accounts_query = MainBankAccount.query.all()
    accounts = {
        acc.id: acc.account_name
        for acc in accounts_query
    }

    account_label = accounts.get(account_id)

    if not account_label:
        flash("Compte introuvable", "error")
        return redirect("/bank-accounts")

    transaction_query = Transaction.query.filter_by(account_id=account_id).all()
    operations = [
        {
            "date": t.date.strftime("%d/%m/%Y"),
            "category": t.category,
            "desc": t.description,
            "amount": f"{t.amount:+} €",
            "amount_numeric": t.amount,
        }
        for t in transaction_query
    ]

    # Résumé
    summary = {
        "total_ops": len(operations),
        "total_in": sum(op["amount_numeric"] for op in operations if op["amount_numeric"] > 0),
        "total_out": sum(op["amount_numeric"] for op in operations if op["amount_numeric"] < 0),
    }

    return render_template("bank/bank_accounts_operation.html", account_id=account_id, account_label=account_label, operations=operations, summary=summary)

@main_bp.route("/depenses/ajouter", methods=["GET", "POST"])
def ajouter_depense():
    accounts_query = MainBankAccount.query.all()

    accounts = [
        {"id": acc.id, "label": acc.account_name, "balance": f"{acc.balance} {acc.monnaie}"}
        for acc in accounts_query
    ]

    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        date = request.form["date"]
        description = request.form.get("description", "")
        account_id = int(request.form["account_id"])

        selected_account = MainBankAccount.query.get(account_id)

        if not selected_account:
            flash("Compte introuvable", "error")
            return redirect("/depenses/ajouter")

        selected_account.balance -= abs(amount)

        transaction = Transaction(
            date=datetime.strptime(date, "%Y-%m-%d"),
            account_label=selected_account.account_name,
            description=description,
            category=category,
            amount=-abs(amount),
            amount_numeric=-abs(amount),
            account_id=account_id,
            user_id=current_user.id
        )

        db.session.add(transaction)
        db.session.commit()

        flash("Dépense ajoutée avec succès.", "success")
        return redirect("/bank-accounts")
    return render_template("bank/depense.html", accounts=accounts)

@main_bp.route("/bank-accounts/add", methods=["POST"])
@login_required
def add_bank_account():

    date = datetime.now()
    bank_origin = request.form["bank_origin"]
    account_name = request.form["account_name"]
    type_account = request.form["type_account"]
    monnaie = request.form["currency"]
    blance = float(request.form["balance"])
    iban = request.form["iban"]

    new_account = MainBankAccount(
        bank_origin=bank_origin,
        account_name=account_name,
        type_account=type_account,
        monnaie=monnaie,
        balance=blance,
        iban=iban,
        user_id= current_user.id
    )

    db.session.add(new_account)
    db.session.commit()
    flash("Compte bancaire ajouté avec succès.", "success")
    return redirect("/bank-accounts")

@main_bp.route("/bank-accounts/<int:account_id>/confirm-activation", methods=["POST"])
def confirm_activation(account_id):
    account = MainBankAccount.query.get(account_id)

    if not account:
        flash("Compte introuvable.", "error")
        return redirect("/bank-accounts")
    
    user_code = request.form["user_code"]
    real_code = request.form["generated_code"]

    if user_code == real_code:
        account.status = True
        db.session.commit()

        flash("Le compte a été activé avec succès.", "success")
    else:
        flash("Le code entré est incorrect.", "error")

    return redirect(f"/bank-accounts/{account_id}")
