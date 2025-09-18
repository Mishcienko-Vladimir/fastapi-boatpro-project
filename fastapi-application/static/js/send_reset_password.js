document.addEventListener("DOMContentLoaded", function () {
    const resetBtn = document.getElementById("reset-password-btn");
    const successMessage = document.getElementById("password-reset-sent");
    const errorMessage = document.getElementById("password-reset-error");

    const userEmailInput = document.getElementById("user-email");
    const resetPasswordInput = document.getElementById("reset-password-url");

    if (!resetBtn || !userEmailInput || !resetPasswordInput) return;

    const userEmail = userEmailInput.value.trim();
    const resetPasswordURL = resetPasswordInput.value;

    resetBtn.addEventListener("click", async (event) => {
        event.preventDefault();

        if (successMessage) successMessage.classList.add("d-none");
        if (errorMessage) errorMessage.classList.add("d-none");

        try {
            const response = await fetch(resetPasswordURL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email: userEmail })
            });

            if (response.ok) {
                if (successMessage) {
                    successMessage.classList.remove("d-none");
                }
                // Меняем текст кнопки
                resetBtn.textContent = "Проверьте почту";
                resetBtn.disabled = true;
            } else {
                // Ошибка от сервера
                if (errorMessage) {
                    errorMessage.classList.remove("d-none");
                }
            }
        } catch (error) {
            console.error("Ошибка сети:", error);
            if (errorMessage) {
                errorMessage.classList.remove("d-none");
            }
        }
    });
});