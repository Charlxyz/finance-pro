function bankAmount() {
    fetch("/api/get/bank_amount", { method: "GET" })
        .then(res => res.json())
        .then(data => {
            document.getElementById("amounnt-bank-main").innerText = data.bank_amount.toFixed(2) + " €";
        });
};

function LastDepence3() {
    fetch("/api/get/depence-3")
        .then(res => res.json())
        .then(data => {
            let container = document.getElementById("last-3-depence");
            container.innerHTML = "";

            if (!data.depence_3 || data.depence_3.length === 0) {
                container.innerHTML = `
                    <li class="text-gray-500 text-sm italic">
                        Aucune dépense trouvée pour ce mois.
                    </li>
                `;
                return;
            }

            data.depence_3.forEach(dep => {
                let li = document.createElement("li");
                li.className = "flex justify-between text-gray-700";

                li.innerHTML = `
                    <span>${dep.description}</span>
                    <span class="font-semibold text-red-600">- ${dep.amount.toFixed(2)} €</span>
                `;

                container.appendChild(li);
            });
        })
        .catch(err => {
            console.error("Erreur API depence-3 :", err);

            container.innerHTML = `
                <li class="text-red-600 text-sm italic">
                    Erreur lors du chargement des dépenses.
                </li>
            `;
        });
}

function LastEnter3() {
    fetch("/api/get/enter-3")
        .then(res => res.json())
        .then(data => {
            let container = document.getElementById("last-3-enter");
            container.innerHTML = "";

            if (!data.enter_3 || data.enter_3.length === 0) {
                container.innerHTML = `
                    <li class="text-gray-500 text-sm italic">
                        Aucune dépense trouvée pour ce mois.
                    </li>
                `;
                return;
            }

            data.enter_3.forEach(dep => {
                let li = document.createElement("li");
                li.className = "flex justify-between text-gray-700";

                li.innerHTML = `
                    <span>${dep.description}</span>
                    <span class="font-semibold text-red-600">- ${dep.amount.toFixed(2)} €</span>
                `;

                container.appendChild(li);
            });
        })
        .catch(err => {
            console.error("Erreur API depence-3 :", err);

            container.innerHTML = `
                <li class="text-red-600 text-sm italic">
                    Erreur lors du chargement des dépenses.
                </li>
            `;
        });
}

function loadAccounts() {
    const select = document.getElementById("depence-compte");
    select.innerHTML = `<option value="">Chargement...</option>`;

    fetch("/api/get/accounts")
        .then(res => res.json())
        .then(data => {
            if (!data.success) {
                select.innerHTML = `<option value="">Erreur de chargement</option>`;
                return;
            }

            if (data.accounts.length === 0) {
                select.innerHTML = `<option value="">Aucun compte disponible</option>`;
                return;
            }

            select.innerHTML = `<option value="">Sélectionner un compte</option>`;

            data.accounts.forEach(acc => {
                const option = document.createElement("option");
                option.value = acc.id;
                option.textContent = `${acc.label} (${acc.balance})`;
                select.appendChild(option);
            });
        })
        .catch(() => {
            select.innerHTML = `<option value="">Erreur serveur</option>`;
        });
}

document.addEventListener("DOMContentLoaded", () => {
    bankAmount();
    LastDepence3();
    LastEnter3();
});

function openDepencesModal() {
    document.getElementById("depences-modal").classList.remove("hidden");
    loadAccounts();
}

function closeDepencesModal() {
    document.getElementById("depences-modal").classList.add("hidden");
}

function addDepence() {
    const description = document.getElementById("depence-description").value;
    const amount = parseFloat(document.getElementById("depence-amount").value);
    const date = document.getElementById("depence-date").value;
    const compte = document.getElementById("depence-compte").value;
    const category = document.getElementById("depence-category").value;

    fetch("/api/post/add_depence", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({  
            description: description,
            amount: amount,
            date: date,
            account_id: compte,
            category: category
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            closeDepencesModal();
            window.location.reload();
        } else {
            alert("Erreur lors de l'ajout de la dépense.");
        }
    });
}