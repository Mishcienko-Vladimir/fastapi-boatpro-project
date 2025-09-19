document.addEventListener("DOMContentLoaded", function () {
    const logoutUrl = document.getElementById("logout-url").value;
    const logoutBtn = document.getElementById("btn-exit");

    if (logoutBtn) {
        logoutBtn.addEventListener("click", async (event) => {
            event.preventDefault();

            try {
                const response = await fetch(logoutUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                });

                if (response.ok) {
                    location.href = "/";
                } else {
                    alert("Ошибка при выходе. Попробуйте снова.");
                }
            } catch (error) {
                console.error("Ошибка сети:", error);
                alert("Ошибка сети. Попробуйте снова.");
            }
        });
    }
});