from flask import Blueprint, flash, request, jsonify, session
import random
from ..extensions import db
from flask_login import current_user
from ..models import User

twofa_bp = Blueprint("twofa_bp", __name__)

# Stocker temporairement un code
TEMP_2FA_CODE = None

@twofa_bp.route("/account/activate/send", methods=["POST"])
@twofa_bp.route("/account/status/send", methods=["POST"])
@twofa_bp.route("/account/2fa/send", methods=["POST"])
def send_2fa_code():
    global TEMP_2FA_CODE

    # Génère un code 2FA
    TEMP_2FA_CODE = str(random.randint(100000, 999999))

    # Log interne (remplace par email + SMS ensuite)
    print("CODE 2FA :", TEMP_2FA_CODE)

    return jsonify({"success": True})

@twofa_bp.route("/account/2fa/verify", methods=["POST"])
def verify_2fa():
    global TEMP_2FA_CODE

    data = request.get_json()
    code = data.get("code")

    if code == TEMP_2FA_CODE:
        # Marque l’utilisateur comme ayant activé la 2FA
        current_user.double_auth_enabled = True
        db.session.commit()
        TEMP_2FA_CODE = None
        flash("Authentification a deux facteurs activé avec succes.", "success")
        return jsonify({"valid": True})

    return jsonify({"valid": False})

@twofa_bp.route("/account/2fa/disable", methods=["POST"])
def disable_2fa():
    current_user.double_auth_enabled = False
    db.session.commit()

    flash("Authentification a deux facteurs désactivé avec succes.", "success")

    return jsonify({"success": True})

@twofa_bp.route("/account/phone/verify", methods=["POST"])
def verify_activation_code():
    global TEMP_2FA_CODE

    data = request.get_json()
    code = data.get("code")

    if code == TEMP_2FA_CODE:
        # Marque l’utilisateur comme ayant activé la 2FA
        current_user.phone_number = data.get("phone_number")
        db.session.commit()
        TEMP_2FA_CODE = None

        flash("Numéros de téléphone ajouté avec succes", "success")

        return jsonify({"valid": True})

    return jsonify({"valid": False})

@twofa_bp.route("/account/status/verify", methods=["POST"])
def verify_account():
    global TEMP_2FA_CODE

    data = request.get_json()
    code = data.get("code")

    if code == TEMP_2FA_CODE:
        # Marque l’utilisateur comme ayant activé la 2FA
        current_user.certified = True
        db.session.commit()
        TEMP_2FA_CODE = None
        flash("Compte certifié avec succes.", "success")
        return jsonify({"valid": True})

    return jsonify({"valid": False})
