function openDetailModal(data) {
    document.getElementById("modal-title").textContent = data.title;
    document.getElementById("modal-type").textContent = data.type;
    document.getElementById("modal-quantity").textContent = data.quantity;
    document.getElementById("modal-value").textContent = data.value;
    document.getElementById("modal-performance").textContent = data.performance;
    document.getElementById("modal-description").textContent = data.description;

    document.getElementById("modal-overlay").classList.remove("hidden");
}

document.getElementById("close-modal").addEventListener("click", () => {
    document.getElementById("modal-overlay").classList.add("hidden");
});

document.getElementById("modal-overlay").addEventListener("click", (e) => {
    if(e.target.id === "modal-overlay"){
        document.getElementById("modal-overlay").classList.add("hidden");
    }
});