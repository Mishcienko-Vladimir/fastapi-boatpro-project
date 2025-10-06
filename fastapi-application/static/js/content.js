function changeMainImage(element) {
    const mainImg = document.getElementById('main-img');
    if (!mainImg) return;
    mainImg.src = element.src;

    const thumbnails = document.querySelectorAll('.thumbnails img');
    thumbnails.forEach(img => img.classList.remove('active'));
    element.classList.add('active');
}

function changeImage(direction) {
    const images = document.querySelectorAll('.thumbnails img');
    if (images.length === 0) return;

    let currentIndex = 0;
    if (localStorage.getItem('currentIndex')) {
        currentIndex = parseInt(localStorage.getItem('currentIndex'), 10);
    }

    currentIndex += direction;

    if (currentIndex < 0) {
        currentIndex = images.length - 1;
    } else if (currentIndex >= images.length) {
        currentIndex = 0;
    }

    localStorage.setItem('currentIndex', currentIndex);

    const selectedImage = images[currentIndex];
    changeMainImage(selectedImage);
}


document.addEventListener('DOMContentLoaded', function () {
    // Обработка .product-link
    if (document.querySelector('.product-link') && document.querySelector('.product')) {
        document.querySelectorAll('.product-link').forEach(link => {
            const product = link.closest('.product');

            if (product) {
                link.addEventListener('mouseenter', () => {
                    product.classList.add('active');
                });

                link.addEventListener('mouseleave', () => {
                    product.classList.remove('active');
                });
            }
        });
    }

    // Обработка миниатюр
    const thumbnails = document.querySelectorAll('.thumbnails img');
    if (thumbnails.length > 0) {
        thumbnails.forEach(img => {
            img.addEventListener('click', function () {
                changeMainImage(this);
            });
        });
    }

    // Обработка вкладок
    const tabs = document.querySelectorAll('.nav-link');
    if (tabs.length > 0) {
        tabs.forEach(tab => {
            tab.addEventListener('click', function (e) {
                e.preventDefault();

                tabs.forEach(t => t.classList.remove('active'));
                this.classList.add('active');

                const tabId = this.getAttribute('data-tab');
                if (!tabId) return;

                const tabPanes = document.querySelectorAll('.tab-pane');
                tabPanes.forEach(pane => pane.classList.remove('active'));

                const activePane = document.getElementById(tabId);
                if (activePane) {
                    activePane.classList.add('active');
                }
            });
        });
    }

    // Кнопки "предыдущее/следующее"
    const prevButton = document.querySelector('.nav-button.prev');
    const nextButton = document.querySelector('.nav-button.next');

    if (prevButton) {
        prevButton.addEventListener('click', () => changeImage(-1));
    }

    if (nextButton) {
        nextButton.addEventListener('click', () => changeImage(1));
    }
});