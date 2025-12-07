function showFlashMessage(type, message) {
    const container = document.getElementById("flash-container");

    const colors = {
        success: "bg-green-600",
        error: "bg-red-600",
        warning: "bg-yellow-600",
        info: "bg-blue-600"
    };

    const box = document.createElement("div");
    box.className =
        `${colors[type] || colors.info} text-white px-5 py-3 rounded-lg shadow-lg flex items-center justify-between transform transition-all duration-300 opacity-0 translate-x-10`;
    
    box.innerHTML = `
        <span class="font-medium">${message}</span>
        <button class="ml-4 text-white text-xl leading-none" onclick="this.parentElement.remove()">&times;</button>
    `;

    container.appendChild(box);

    // Animation d’apparition
    setTimeout(() => {
        box.classList.remove("opacity-0", "translate-x-10");
    }, 50);

    // Disparition automatique
    setTimeout(() => {
        box.classList.add("opacity-0", "translate-x-10");
        setTimeout(() => box.remove(), 300);
    }, 4000);
}

// Affiche les messages envoyés par Flask
window.addEventListener("DOMContentLoaded", () => {
    flashMessages.forEach(([type, message]) => {
        showFlashMessage(type, message);
    });
});
