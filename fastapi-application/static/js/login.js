document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    const usernameInput = form.elements["username"];
    const passwordInput = form.elements["password"];
    const rememberMeCheckbox = document.getElementById("remember-me");
    const loginUrl = document.getElementById("login-url").value;

    // Загрузка сохранённых данных
    if (localStorage.getItem("rememberMe") === "true") {
        usernameInput.value = localStorage.getItem("username");
        passwordInput.value = localStorage.getItem("password");
        rememberMeCheckbox.checked = true;
    }

    // Обработка отправки формы
    if (form) {
        form.addEventListener("submit", async function (event) {
            event.preventDefault();

            const username = usernameInput.value;
            const password = passwordInput.value;

            // Сохраняем данные, если пользователь выбрал "Запомнить меня"
            if (rememberMeCheckbox.checked) {
                localStorage.setItem("username", username);
                localStorage.setItem("password", password);
                localStorage.setItem("rememberMe", "true");
            } else {
                localStorage.removeItem("username");
                localStorage.removeItem("password");
                localStorage.removeItem("rememberMe");
            }

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

                    if (response.status === 429) {
                        errorDiv.innerText = "Слишком много попыток. Попробуйте позже.";
                    } else if (errorDetails.detail === "LOGIN_BAD_CREDENTIALS") {
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
    }
});