function handleSearch() {
    const query = document.getElementById("search-input").value.trim();
    if (query) {
        const searchUrl = document.getElementById("search-url").value;
        window.location.href = `${searchUrl}?query=${encodeURIComponent(query)}`;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    // Обработка клика на иконке поиска
    const searchIcon = document.querySelector(".search-btn ion-icon");
    if (searchIcon) {
        searchIcon.addEventListener("click", handleSearch);
    }

    // Обработка нажатия Enter в поле поиска
    const searchInput = document.getElementById("search-input");
    if (searchInput) {
        searchInput.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                handleSearch();
            }
        });
    }
});