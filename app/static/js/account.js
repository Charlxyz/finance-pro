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
