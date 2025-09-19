document.addEventListener("DOMContentLoaded", function () {
    const loadingIndicator = document.getElementById('loading-indicator');
    const missingTokenAlert = document.getElementById('missing-token-alert');
    const verificationErrorAlert = document.getElementById('verification-error-alert');
    const verificationURL = document.getElementById("verify-email").value;;

    loadingIndicator.classList.remove("d-none");

    (async () => {
        const params = new URLSearchParams(window.location.search);
        const token = params.get('token');

        if (!token) {
            missingTokenAlert.classList.remove('d-none');
            loadingIndicator.classList.add('d-none');
            return;
        }

        try {
            const response = await fetch(verificationURL, {
                method: 'POST',
                headers: {
                            'Content-Type': 'application/json'
                },
                body: JSON.stringify({ token })
            });
            loadingIndicator.classList.add('d-none');

            if (response.ok) {
                window.location.href = "/";
            } else {
                verificationErrorAlert.classList.remove('d-none');
                loadingIndicator.classList.add('d-none');
            }
        } catch (error) {
            console.error("Ошибка сети:", error);
            verificationErrorAlert.classList.remove('d-none');
        }
    })();
});