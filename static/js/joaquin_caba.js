document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.mostrarComprobante').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const targetId = button.getAttribute('data-target');
            const imgContainer = document.querySelector(targetId);
            const overlay = document.querySelector('.overlay');

            // Ocultar todas las imágenes primero
            document.querySelectorAll('.compIms').forEach(container => {
                container.style.display = 'none';
            });

            // Mostrar la imagen seleccionada y el overlay
            if (imgContainer) {
                imgContainer.style.display = 'block';
                const img = imgContainer.querySelector('.comprobante-img');
                if (img) {
                    img.style.display = 'block';
                }
                overlay.style.display = 'block';
            }
        });
    });

    // Ocultar la imagen cuando se haga clic en el overlay
    document.querySelector('.overlay').addEventListener('click', () => {
        document.querySelectorAll('.compIms').forEach(container => {
            container.style.display = 'none';
        });
        document.querySelector('.overlay').style.display = 'none';
    });

    // Ocultar la imagen cuando se haga clic en la "X"
    document.querySelectorAll('.cerrar-imagen').forEach(button => {
        button.addEventListener('click', () => {
            button.closest('.compIms').style.display = 'none';
            document.querySelector('.overlay').style.display = 'none';
        });
    });
});