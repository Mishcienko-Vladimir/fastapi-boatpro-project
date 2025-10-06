document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(".btn-delete");
    const favoritesDelUrlInput = document.getElementById("favorites-del-url");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", async function () {
            const favoriteId = this.getAttribute("data-favorite-id");

            if (!favoriteId) {
                alert("ID товара не указан.");
                return;
            }

            try {
                const response = await fetch(`${favoritesDelUrlInput.value}?favorite_id=${favoriteId}`, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                if (response.ok) {
                    location.reload();
                } else {
                    const errorData = await response.json();
                    alert(`Ошибка: ${errorData.detail || "Не удалось удалить товар."}`);
                }
            } catch (error) {
                console.error("Ошибка при удалении:", error);
                alert("Произошла ошибка при удалении товара.");
            }
        });
    });

    // Функция для добавления товара в избранное
    const btnAddFavorites = document.getElementById('btnAddFavorites');
    const favoritesAddUrlInput = document.getElementById("favorites-add-url");

    if (btnAddFavorites && favoritesAddUrlInput) {
        const userId = parseInt(document.getElementById("user-id").value);
        const productId = parseInt(document.getElementById("product-id").value);

        btnAddFavorites.addEventListener("click", async (event) => {
            event.preventDefault();

            if (!userId) {
                alert("Авторизуйтесь или зарегистрируйтесь, чтобы добавить товар в избранное.");
                return;
        }

            try {
                const response = await fetch(favoritesAddUrlInput.value, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        user_id: userId,
                        product_id: productId
                    })
                });

                if (response.ok) {
                    const favoritesIcon = document.querySelector('.nav-right .favorites-btn ion-icon');

                    if (favoritesIcon) {
                        favoritesIcon.setAttribute('name', 'heart');
                        favoritesIcon.style.color = '#ff0000';
                        favoritesIcon.style.transform = 'scale(1.5)';
                        favoritesIcon.style.transition = 'transform 0.3s ease, color 0.3s ease';

                        setTimeout(() => {
                            favoritesIcon.setAttribute('name', 'heart-outline');
                            favoritesIcon.style.color = '';
                            favoritesIcon.style.transform = 'scale(1)';
                        }, 1000);
                    }
                } else {
                    const errorData = await response.json();
                    alert("Товар уже в избранном.");
                }
            } catch (error) {
                console.error("Ошибка при добавлении:", error);
                alert("Произошла ошибка при добавлении товара.");
            }
        });
    }
});