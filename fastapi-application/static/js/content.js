document.querySelectorAll('.product-link').forEach(link => {
    const product = link.closest('.product');

    link.addEventListener('mouseenter', () => {
        product.classList.add('active');
    });

    link.addEventListener('mouseleave', () => {
        product.classList.remove('active');
    });
});