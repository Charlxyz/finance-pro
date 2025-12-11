function openActivateModal(button) {
    const accountId = button.dataset.accountId;

    console.log("ID récupéré :", accountId);

    if (!accountId) {
        console.error("Aucun ID trouvé sur le bouton !");
        return;
    }

    document.getElementById("activate-modal").classList.remove("hidden");
}

function closeActivateModal() {
    document.getElementById("activate-modal").classList.add("hidden");
}

// ===== POPUP EMAIL =====

function openEmailConfirmModal() {
    closeActivateModal();

    const modal = document.getElementById("email-confirm-modal");
    modal.classList.remove("hidden");

    // Génère le code
    const code = Math.floor(100000 + Math.random() * 900000);

    document.getElementById("generated-code").textContent = code;
    document.getElementById("hidden-generated-code").value = code;

    // Ajout : Envoie l’état de la case "compte principal"
    document.getElementById("hidden-set-main").value =
        document.getElementById("main_account").checked ? "1" : "";

    console.log("CODE DE CONFIRMATION :", code);
}


function closeEmailConfirmModal() {
    document.getElementById("email-confirm-modal").classList.add("hidden");
}

document.getElementById("email-confirm-modal").addEventListener("click", (e) => {
    if (e.target.id === "email-confirm-modal") {
        closeEmailConfirmModal();
    }
});
