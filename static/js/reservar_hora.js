document.querySelectorAll('.listaDeCanchas img').forEach(img => {
    img.addEventListener('click', (event) => {
        document.querySelectorAll('.listaDeCanchas img.active').forEach(activeImg => {
            activeImg.classList.remove('active');
            activeImg.style.left = '0';
            activeImg.style.top = '0';
        });
        img.classList.add('active');
        img.style.left = '50%';
        img.style.top = '50%';
        event.stopPropagation();
    });
});

document.addEventListener('click', () => {
    document.querySelectorAll('.listaDeCanchas img.active').forEach(activeImg => {
        activeImg.classList.remove('active');
        activeImg.style.left = '0';
        activeImg.style.top = '0';
    });
});

