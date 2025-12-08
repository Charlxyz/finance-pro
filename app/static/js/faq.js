document.addEventListener("DOMContentLoaded", function () {
    const faqButtons = document.querySelectorAll(".faq-btn");

    faqButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            const content = btn.nextElementSibling;
            const icon = btn.querySelector(".faq-icon");

            if (!content || !icon) return;

            // Toggle visibilité
            content.classList.toggle("hidden");

            // Toggle icône
            if (content.classList.contains("hidden")) {
                icon.textContent = "+";
            } else {
                icon.textContent = "-";
            }
        });
    });
});
