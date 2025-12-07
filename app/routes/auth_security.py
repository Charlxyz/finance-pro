from flask import Blueprint, request, jsonify, session
import random

twofa_bp = Blueprint("twofa_bp", __name__)

# Stocker temporairement un code
TEMP_2FA_CODE = None


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
        session["2fa_enabled"] = True
        TEMP_2FA_CODE = None
        return jsonify({"valid": True})

    return jsonify({"valid": False})
