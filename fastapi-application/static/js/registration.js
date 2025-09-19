document.addEventListener("DOMContentLoaded", function () {
    const verifyUrlInput = document.getElementById("verify-url");
    const registerUrlInput = document.getElementById("register-url");
    const btnRegister = document.getElementById("btn-register");

    const registerRequestError = document.getElementById("register-request-error");
    const registerLoadingIndicator = document.getElementById("register-loading-indicator");

    const registerFirstNameInput = document.getElementById("register-first-name");
    const registerEmailInput = document.getElementById("register-email");
    const registerPasswordInput = document.getElementById("register-password");

    if (
        !verifyUrlInput ||
        !registerUrlInput ||
        !btnRegister ||
        !registerEmailInput ||
        !registerPasswordInput ||
        !registerFirstNameInput
    ) return;

    const requestVerificationURL = verifyUrlInput.value;
    const requestRegisterURL = registerUrlInput.value;

    btnRegister.addEventListener("click", async (event) => {
        event.preventDefault();

        const userEmailRegister = registerEmailInput.value.trim();
        const userPasswordRegister = registerPasswordInput.value.trim();
        const userFirstNameRegister = registerFirstNameInput.value.trim();

        if (registerRequestError) registerRequestError.classList.add("d-none");

        btnRegister.classList.add("d-none");
        registerLoadingIndicator.classList.remove("d-none");

        try {
            const response = await fetch(requestRegisterURL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: userEmailRegister,
                    password: userPasswordRegister,
                    first_name: userFirstNameRegister
                })
            });

            registerLoadingIndicator.classList.add("d-none");
            btnRegister.classList.remove("d-none");

            if (response.ok) {
                const responseVerify = await fetch(requestVerificationURL, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ email: userEmailRegister })
                });
                alert("На вашу почту отправлено письмо для подтверждения регистрации.");
                window.location.href = "/";
            } else {
                if (registerRequestError) {
                    registerRequestError.classList.remove("d-none");
                }
            }
        } catch (error) {
            console.error("Ошибка сети:", error);
            alert("Произошла ошибка. Попробуйте снова.");
            registerLoadingIndicator.classList.add("d-none");
            btnRegister.classList.remove("d-none");
        }
    });
});