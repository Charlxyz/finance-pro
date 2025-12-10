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
    closeActivateModal(); // ferme la première popup

    const modal = document.getElementById("email-confirm-modal");
    modal.classList.remove("hidden");

    // Génération d’un code à 6 chiffres
    const code = Math.floor(100000 + Math.random() * 900000);

    // Affichage du code dans la popup
    document.getElementById("generated-code").textContent = code;

    // Stockage du code dans le champ caché pour Flask
    document.getElementById("hidden-generated-code").value = code;

    // Affichage dans la console (simulateur d'envoi mail)
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
