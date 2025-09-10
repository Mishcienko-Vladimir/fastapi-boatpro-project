document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    if (!form) return;

    // Получаем URL из скрытого input
    const loginUrl = document.getElementById("login-url").value;

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = form.elements["username"].value;
        const password = form.elements["password"].value;

        const data = `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;

        try {
            const response = await fetch(loginUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: data
            });

            if (!response.ok) {
                const errorDetails = await response.json();
                const errorDiv = document.getElementById("login-error");

                if (errorDetails.detail === "LOGIN_BAD_CREDENTIALS") {
                    errorDiv.innerText = "Неверный логин или пароль.";
                } else {
                    errorDiv.innerText = "Ошибка при входе. Попробуйте еще раз.";
                }

                errorDiv.classList.add("show");

                setTimeout(() => {
                    errorDiv.classList.remove("show");
                }, 5000);
            } else {
                location.href = "/"; // Перенаправление после успешного входа
            }
        } catch (error) {
            console.error("Ошибка сети:", error);
            const errorDiv = document.getElementById("login-error");
            errorDiv.innerText = "Ошибка сети. Попробуйте снова.";
            errorDiv.classList.add("show");

            setTimeout(() => {
                errorDiv.classList.remove("show");
            }, 5000);
        }
    });
});