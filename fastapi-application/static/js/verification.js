document.addEventListener("DOMContentLoaded", function () {
    const verifyForm = document.getElementById("email-verification-form");
    const verifyBtn = verifyForm?.querySelector(".btnEmailVerify");
    const verificationEmailSent = document.getElementById("verification-email-sent");
    const verificationRequestError = document.getElementById("verification-request-error");
    const loadingIndicator = document.getElementById("loading-indicator");

    const userEmailInput = document.getElementById("user-email");
    const verifyUrlInput = document.getElementById("verify-url");

    if (!verifyBtn || !loadingIndicator || !userEmailInput || !verifyUrlInput) return;

    const userEmail = userEmailInput.value.trim();
    const requestVerificationURL = verifyUrlInput.value;

    verifyBtn.addEventListener("click", async (event) => {
        event.preventDefault();

        if (verificationEmailSent) verificationEmailSent.classList.add("d-none");
        if (verificationRequestError) verificationRequestError.classList.add("d-none");

        loadingIndicator.classList.remove("d-none");
        verifyBtn.style.display = "none";

        try {
            const response = await fetch(requestVerificationURL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email: userEmail })
            });

            if (response.ok) {
                loadingIndicator.classList.add("d-none");

                if (verificationEmailSent) {
                    verificationEmailSent.classList.remove("d-none");
                }
            } else {
                loadingIndicator.classList.add("d-none");

                if (verificationRequestError) {
                    verificationRequestError.classList.remove("d-none");
                }
            }
        } catch (error) {
            console.error("Ошибка сети:", error);
            alert("Ошибка сети. Попробуйте снова.");

            loadingIndicator.classList.add("d-none");
            if (verifyBtn) {
                verifyBtn.style.display = "block";
            }
        }
    });
});