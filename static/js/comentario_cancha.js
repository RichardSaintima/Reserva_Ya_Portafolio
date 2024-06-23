document.addEventListener("DOMContentLoaded", function () {
    const estrellas = document.querySelectorAll(".estrella");
    const comentario = document.getElementById('comentario');
    const charCount = document.getElementById('charCount');
    const maxChars = comentario.getAttribute('maxlength');
    
    estrellas.forEach(function (estrella) {
        estrella.addEventListener("click", function () {
            const value = parseInt(this.getAttribute("data-value"));
            // Cambiar el color de todas las estrellas hasta la que se ha seleccionado
            estrellas.forEach(function (e) {
                if (e.getAttribute("data-value") <= value) {
                    e.style.color = "#f7b500"; // Cambiar a tu color deseado
                } else {
                    e.style.color = "#0790f88e"; // Cambiar a tu color original
                }
            });
            // Actualizar el campo oculto con la calificación seleccionada
            document.getElementById("calificacion_seleccionada").value = value;
        });
    });

    comentario.addEventListener('input', function() {
        const currentLength = comentario.value.length;
        charCount.textContent = `${currentLength}/${maxChars} caracteres`;
    });

});