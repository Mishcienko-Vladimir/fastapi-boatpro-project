document.addEventListener("DOMContentLoaded", function () {
    const verifyUrl = document.getElementById("verify-url")?.value;
    const verifyForm = document.getElementById("email-verification-form");

    if (!verifyForm || !verifyUrl) return;

    const verifyBtn = verifyForm.querySelector(".btnEmailVerify");
    if (!verifyBtn) return;

    // Получаем email из шаблона
    const userEmail = "{{ user.email }}";

    verifyBtn.addEventListener("click", async (event) => {
        event.preventDefault();

        try {
            const response = await fetch(verifyUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email: userEmail })
            });

            if (response.ok) {
                // Удаляем кнопку и добавляем сообщение о подтверждении
                verifyBtn.remove();
                const confirmation = document.createElement("p");
                confirmation.className = "p-confirmation";
                confirmation.innerText = "Почта подтверждена";

                // Добавляем новое сообщение вместо кнопки
                verifyForm.appendChild(confirmation);
            } else {
                alert("Ошибка при отправке запроса на подтверждение. Попробуйте снова.");
            }
        } catch (error) {
            console.error("Ошибка сети:", error);
            alert("Ошибка сети. Попробуйте снова.");
        }
    });
});