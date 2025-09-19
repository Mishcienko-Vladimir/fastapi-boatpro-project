document.addEventListener("DOMContentLoaded", function () {
    const wrapper = document.querySelector('.wrapper');
    const blockContent = document.querySelector('.block-content');
    const loginLink = document.querySelector('.login-link');
    const registerLink = document.querySelector('.register-link');
    const btnPopup = document.querySelector('.login-btn');
    const iconClose = document.querySelector('.icon-close');

    registerLink.addEventListener('click', ()=> {
        wrapper.classList.add('active');
    });

    loginLink.addEventListener('click', ()=> {
        wrapper.classList.remove('active');
    });

    btnPopup.addEventListener('click', () => {
        blockContent.classList.add('hidden');
        setTimeout(() => {
            wrapper.classList.add('active-popup');
        }, 400);
    });

    iconClose.addEventListener('click', () => {
        wrapper.classList.remove('active-popup');
        setTimeout(() => {
            blockContent.classList.remove('hidden');
        }, 400);
    });
});