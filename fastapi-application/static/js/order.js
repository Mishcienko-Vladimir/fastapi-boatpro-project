document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("orderModal");
    const modalContent = document.getElementById("orderModalContent");
    const btnBuy = document.getElementById("btnBuy");

    if (!btnBuy) return;

    if (!modal) return;

    if (!modalContent) return;

    // Закрытие модалки
    const span = modal.querySelector(".close");
    if (span) {
        span.onclick = () => {
            modal.style.display = "none";
        };
    }

    window.onclick = (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    };

    btnBuy.onclick = async () => {
        const userId = document.getElementById("user-id")?.value;
        const productId = document.getElementById("product-id")?.value;
        const priceElement = document.querySelector(".bloc-price-info p");
        const price = priceElement
            ? priceElement.textContent
                  .replace("Цена: ", "")
                  .replace(" ₽", "")
                  .trim()
            : null;

        if (!productId || !price) {
            alert("Не удалось получить данные о товаре");
            return;
        }

        if (!userId) {
            modalContent.innerHTML = `
                <h2>Требуется авторизация</h2>
                <p>Чтобы оформить заказ, войдите или зарегистрируйтесь.</p>
                <button class="btn-buy" onclick="window.location.href='/auth/login'">
                    Войти
                </button>
            `;
        } else {
            try {
                const response = await fetch("/api/v1/pickup-points/");
                if (!response.ok) throw new Error(`Сеть: ${response.status}`);

                const points = await response.json();

                modalContent.innerHTML = `
                    <h2>Оформление заказа</h2>
                    <form id="orderForm">
                        <input type="hidden" name="product_id" value="${productId}">
                        <div class="form-group">
                            <label for="pickupPoint">Пункт самовывоза:</label>
                            <div class="custom-select">
                                <button type="button" class="select-btn" id="selectBtn">
                                    Выберите пункт самовывоза
                                </button>
                                <ul class="select-dropdown" id="selectDropdown" style="display: none;">
                                    ${points.map(p => `
                                        <li data-id="${p.id}">
                                            <strong>${p.name}</strong><br>
                                            <small>${p.address}</small><br>
                                            <em>${p.work_hours}</em>
                                        </li>
                                    `).join("")}
                                </ul>
                                <input type="hidden" name="pickup_point_id" id="pickupPointInput" required>
                            </div>
                        </div>
                        <p>Цена: <strong>${price} ₽</strong></p>
                        <button type="submit" class="btn-buy">Оформить заказ</button>
                    </form>
                `;

                const selectBtn = document.getElementById("selectBtn");
                const dropdown = document.getElementById("selectDropdown");
                const input = document.getElementById("pickupPointInput");

                // Переключение выпадающего списка
                selectBtn.onclick = () => {
                    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
                };

                // Выбор пункта
                dropdown.querySelectorAll("li").forEach(item => {
                    item.onclick = () => {
                        const id = item.getAttribute("data-id");
                        const name = item.querySelector("strong").textContent;
                        input.value = id;
                        selectBtn.textContent = name;
                        dropdown.style.display = "none";
                    };
                });

                // Закрытие при клике вне
                document.addEventListener("click", (e) => {
                    if (!selectBtn.contains(e.target) && !dropdown.contains(e.target)) {
                        dropdown.style.display = "none";
                    }
                });

                // Обработка формы
                const form = document.getElementById("orderForm");
                form.onsubmit = async (e) => {
                    e.preventDefault();
                    if (!input.value) {
                        alert("Выберите пункт самовывоза");
                        return;
                    }

                    const formData = new FormData(form);
                    const data = Object.fromEntries(formData);

                    const createResponse = await fetch("/api/v1/orders/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify(data),
                    });

                    const result = await createResponse.json();

                    if (createResponse.ok) {
                        window.location.href = result.payment_url;
                    } else {
                        alert("Ошибка: " + result.detail);
                    }
                };
            } catch (error) {
                modalContent.innerHTML = `<p>Ошибка: ${error.message}</p>`;
            }
        }

        modal.style.display = "block";
    };
});
