function openConfidentialityModal() {
    document.getElementById("confidentiality-modal").classList.remove("hidden");
}

function closeConfidentialityModal() {
    document.getElementById("confidentiality-modal").classList.add("hidden");
}

// Fermer en cliquant sur l'arrière-plan
document.getElementById("confidentiality-modal").addEventListener("click", (e) => {
    if (e.target.id === "confidentiality-modal") {
        closeConfidentialityModal();
    }
});

function openTwoFAModal() {
    document.getElementById("twofa-modal").classList.remove("hidden");
}

function closeTwoFAModal() {
    document.getElementById("twofa-modal").classList.add("hidden");

    // Reset des étapes
    document.getElementById("step-activate").classList.remove("hidden");
    document.getElementById("step-verify").classList.add("hidden");
    document.getElementById("step-success").classList.add("hidden");
}

function reloadTwoFAModal() {
    window.location.reload();
}

// Simulation : envoi du code 2FA
function sendTwoFACode() {
    fetch("/account/2fa/send", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                document.getElementById("step-activate").classList.add("hidden");
                document.getElementById("step-verify").classList.remove("hidden");
            }
        });
}

// Vérification
function verifyTwoFACode() {
    const code = document.getElementById("twofa-code-input").value;

    fetch("/account/2fa/verify", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ code: code })
    })
    .then(res => res.json())
    .then(data => {
        if (data.valid) {
            document.getElementById("step-verify").classList.add("hidden");
            document.getElementById("step-success").classList.remove("hidden");
        } else {
            alert("Code incorrect");
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("profileVisibility");
    toggle.addEventListener("change", () => {
        const newValue = toggle.checked ? 1 : 0;

        // Appel AJAX vers Flask
        fetch("/account/confidentiality", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                visible: newValue
            })
        })
        .then(response => response.json())
        .then(data => {
            window.location.reload();
        })
        .catch(err => {
            alert("Erreur lors de la mise à jour des paramètres de confidentialité.", err);
        });
    });
});

function openStatusAccountModal() {
    document.getElementById("status-account-modal").classList.remove("hidden");
}

function closeStatusAccountModal() {
    document.getElementById("status-account-modal").classList.add("hidden");
}

function reloadStatusAccountModal() {
    window.location.reload();
}

function sendPhoneNumberVerify() {
    fetch("/account/activate/send", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                document.getElementById("step-phone-activate").classList.add("hidden");
                document.getElementById("step-phone-verify").classList.remove("hidden");
            }
        });
}

function verifyActivationCode(phone_number) {
    const code = document.getElementById("activation-code-input").value;
    fetch("/account/phone/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: code,
            phone_number: phone_number
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.valid) {
            document.getElementById("step-phone-verify").classList.add("hidden");
            document.getElementById("step-phone-success").classList.remove("hidden");
            window.location.reload();
        } else {
            alert("Code incorrect");
        }
    });
}

function sendAccountVerify(){
    fetch("/account/status/send", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                document.getElementById("step-account-activate").classList.add("hidden");
                document.getElementById("step-account-verify").classList.remove("hidden");
            }
        });
}

function verifyAccountCode() {
    const code = document.getElementById("account-activation-code-input").value;
    fetch("/account/status/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: code })
    })
    .then(res => res.json())
    .then(data => {
        if (data.valid) {
            document.getElementById("step-account-verify").classList.add("hidden");
            document.getElementById("step-account-success").classList.remove("hidden");
            window.location.reload();
        } else {
            alert("Code incorrect");
        }
    });
}

function closeAccountModal() {
    document.getElementById("status-account-modal").classList.add("hidden");
    // Reset des étapes
    document.getElementById("step-account-activate").classList.remove("hidden");
    document.getElementById("step-account-verify").classList.add("hidden");
    document.getElementById("step-account-success").classList.add("hidden");
}

function openTwoFASettingsModal() {
    document.getElementById("twofa-settings-modal").classList.remove("hidden");
}

function closeTwoFASettingsModal() {
    document.getElementById("twofa-settings-modal").classList.add("hidden");
}

function reloadTwoFASettingsModal() {
    window.location.reload();
}

function verifyDisable2af() {
    fetch("/account/2fa/disable", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                closeTwoFASettingsModal();
                window.location.reload();
            }
        });
}

function monthlySalary() {
    fetch("/api/get/salary", { method: "GET" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("monthly-salary-amount").innerText = data.salary.toFixed(2) + " €";
        });
}

function monthlyDepence() {
    fetch("/api/get/depence", { method: "GET" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("monthly-depence-amount").innerText = data.depence.toFixed(2) + " €";
        });
}

function bankAmount() {
    fetch("/api/get/bank_amount", { method: "GET" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("bank-amount").innerText = data.bank_amount.toFixed(2) + " €";
        });
}

document.addEventListener("DOMContentLoaded", () => {
    monthlySalary();
    monthlyDepence();
    bankAmount();
});
