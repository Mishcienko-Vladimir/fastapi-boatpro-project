document.addEventListener("DOMContentLoaded", function () {
    const loadingIndicator = document.getElementById('loading-indicator');
    const btnRecoveryEmail = document.getElementById("btn-recovery-email");
    const successMessage = document.getElementById("password-reset-sent");
    const errorMessage = document.getElementById("password-reset-error");

    const userEmailInput = document.getElementById("recovery-email");
    const resetPasswordInput = document.getElementById("reset-password-url");

    if (!btnRecoveryEmail || !userEmailInput || !resetPasswordInput) return;

    const resetPasswordURL = resetPasswordInput.value;

    btnRecoveryEmail.addEventListener("click", async (event) => {
        event.preventDefault();

        const userEmail = userEmailInput.value.trim();

        btnRecoveryEmail.classList.add("d-none");
        loadingIndicator.classList.remove("d-none");

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

            loadingIndicator.classList.add("d-none");
            btnRecoveryEmail.classList.remove("d-none");

            if (response.ok) {
                if (successMessage) {
                    successMessage.classList.remove("d-none");
                }
                // Меняем текст кнопки
                btnRecoveryEmail.textContent = "Проверьте почту";
                btnRecoveryEmail.disabled = true;
            } else {
                // Ошибка от сервера
                if (errorMessage) {
                    errorMessage.classList.remove("d-none");
                }
            }
        } catch (error) {
            console.error("Ошибка сети:", error);
            alert("Произошла ошибка. Попробуйте снова.");
            loadingIndicator.classList.add("d-none");
            btnRecoveryEmail.classList.remove("d-none");
        }
    });
});