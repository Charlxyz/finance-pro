from datetime import date, datetime
from flask import Blueprint, redirect, render_template, request, flash
from flask_login import current_user, login_required, logout_user
from ..models import User, MainBankAccount, Transaction
from ..extensions import db

# Création du blueprint
main_bp = Blueprint("main", __name__)

# Autres routes
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

@main_bp.route("/account/confidentiality", methods=["POST"])
@login_required
def update_confidentiality():
    data = request.get_json()

    current_user.anonymous = data.get("visible", current_user.anonymous)
    db.session.commit()

    flash("Paramètres de confidentialité mis à jour.", "success")

    return {"status": "success"}, 200

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
    account = MainBankAccount.query.filter_by(
        id=account_id,
        user_id=current_user.id
    ).first()

    if not account:
        flash("Compte introuvable.", "error")
        return redirect("/bank-accounts")

    user_code = request.form.get("user_code", "")
    real_code = request.form.get("generated_code", "")
    set_main = request.form.get("set_main")

    if user_code != real_code:
        flash("Le code entré est incorrect.", "error")
        return redirect(f"/bank-accounts/{account_id}")

    account.status = True

    if set_main:
        MainBankAccount.query.filter(
            MainBankAccount.user_id == current_user.id,
            MainBankAccount.id != account.id
        ).update({"main_account": False})

        account.main_account = True

    db.session.commit()

    flash("Le compte a été activé avec succès.", "success")
    return redirect(f"/bank-accounts/{account_id}")

@main_bp.route("/api/get/salary")
def get_salary():
    today = date.today()
    start_month = date(today.year, today.month, 1)

    salary = Transaction.query.filter_by(
        id=current_user.id,
        category="Salaire"
    ).filter(
        Transaction.date >= start_month,
        Transaction.date <= today
    ).first()

    total_salary = sum(s.amount for s in salary) if salary else 0.0

    return { "salary": abs(total_salary) if salary else 0.0 }

@main_bp.route("/api/get/depence")
def get_depence():
    today = date.today()
    start_month = date(today.year, today.month, 1)

    depence = Transaction.query.filter_by(
        id=current_user.id,
    ).filter(
        Transaction.date >= start_month,
        Transaction.date <= today,
        Transaction.amount < 0
    ).all()

    total_depence = sum(d.amount for d in depence)

    return { "depence": abs(total_depence) if total_depence else 0.0 }

@main_bp.route("/api/get/depence-3")
def get_depence_3():
    today = date.today()
    start_month = date(today.year, today.month, 1)

    depences = (
        Transaction.query
            .filter_by(user_id=current_user.id)
            .filter(
                Transaction.date >= start_month,
                Transaction.date <= today,
                Transaction.amount < 0
            )
            .order_by(Transaction.date.desc())
            .limit(3)
            .all()
    )

    depence_list = [{
        "description": d.description or "Sans description",
        "date": d.date.strftime("%d/%m/%Y"),
        "amount": abs(d.amount)
    } for d in depences]

    return { "depence_3": depence_list }

@main_bp.route("/api/get/enter-3")
def get_enter_3():
    today = date.today()
    start_month = date(today.year, today.month, 1)

    enter = (
        Transaction.query
            .filter_by(user_id=current_user.id)
            .filter(
                Transaction.date >= start_month,
                Transaction.date <= today,
                Transaction.amount > 0
            )
            .order_by(Transaction.date.desc())
            .limit(3)
            .all()
    )

    enter_list = [{
        "description": d.description or "Sans description",
        "date": d.date.strftime("%d/%m/%Y"),
        "amount": abs(d.amount)
    } for d in enter]

    return { "enter_3": enter_list }

@main_bp.route("/api/get/bank_amount")
def get_bank_amount():
    accounts = MainBankAccount.query.filter_by(user_id=current_user.id, main_account=1).all()
    total_amount = sum(acc.balance for acc in accounts) if accounts else 0.0

    return { "bank_amount": total_amount }

@main_bp.route("/api/add/depence/<int:account_id>", methods=["POST"])
def add_depence(account_id):
    account = MainBankAccount.query.get(account_id)
    
    if not account:
        flash("Compte introuvable.", "error")
        return {"status": "error"}, 404
    
    data = request.get_json()
    amount = float(data.get("amount", 0))
    category = data.get("category", "Autre")
    date_str = data.get("date", "")
    description = data.get("description", "")
    date_obj = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.now()
    account.balance -= abs(amount)
    
    transaction = Transaction(
        date=date_obj,
        account_label=account.account_name,
        description=description,
        category=category,
        amount=-abs(amount),
        account_id=account_id,
        user_id=current_user.id
    ) 

    db.session.add(transaction)
    db.session.commit()

    flash("Dépense ajoutée avec succès.", "success")
    return {"status": "success"}, 200

@main_bp.route("/api/get/accounts")
def api_get_accounts():
    accounts_query = MainBankAccount.query.all()

    accounts = [
        {
            "id": acc.id,
            "label": acc.account_name,
            "balance": f"{acc.balance} {acc.monnaie}"
        }
        for acc in accounts_query
    ]

    return {"success": True, "accounts": accounts}
