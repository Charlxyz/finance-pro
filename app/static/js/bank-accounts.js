function openAddBankModal() {
    document.getElementById("add-bank-modal").classList.remove("hidden");
}

function closeAddBankModal() {
    document.getElementById("add-bank-modal").classList.add("hidden");
}

// Fermer si on clique en dehors
document.getElementById("add-bank-modal").addEventListener("click", (e) => {
    if (e.target.id === "add-bank-modal") {
        closeAddBankModal();
    }
});
