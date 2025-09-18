document.addEventListener("DOMContentLoaded", function () {
    const loadingIndicator = document.getElementById('loading-indicator');
    const passwordInput = document.getElementById('password-new');
    const resetBtn = document.getElementById('change-password');
    const verificationURL = document.getElementById("password-reset").value;

    resetBtn.addEventListener("click", async (event) => {
        event.preventDefault();

        resetBtn.classList.add("d-none");
        loadingIndicator.classList.remove("d-none");

        const newPassword = passwordInput.value.trim();
        const params = new URLSearchParams(window.location.search);
        const token = params.get('token');

        // Проверка наличия токена
        if (!token) {
            alert("Токен отсутствует. Повторите попытку.");
            return;
        }

        try {
            const response = await fetch(verificationURL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ token, password: newPassword })
            });

            loadingIndicator.classList.add("d-none");
            resetBtn.classList.remove("d-none");

            if (response.ok) {
                // Успешный сброс пароля — переходим на главную
                window.location.href = "/";
            } else {
                const errorData = await response.json();
                alert(`Ошибка: ${errorData.detail || "Не удалось сбросить пароль."}`);
            }
        } catch (error) {
            console.error("Ошибка сети:", error);
            alert("Произошла ошибка. Попробуйте снова.");
            loadingIndicator.classList.add("d-none");
            resetBtn.classList.remove("d-none");
        }
    });
});