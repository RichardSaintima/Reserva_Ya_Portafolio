window.onload = function () {    
    const TIEMPO_INTERVALO_MILESIMAS_SEG = 3000; // Ajustado a 3 segundos
    let posicionActual = 0;
    const $imagenes = document.querySelectorAll('.imagen'); // Seleccionar todas las imágenes
    const $botonAvanzar = document.querySelector('#avanzar');
    const $botonRetroceder = document.querySelector('#retroceder');
    let intervalo;

    /**
     * Funcion que cambia la foto en la siguiente posicion
     */
    function pasarFoto() {
        if(posicionActual >= $imagenes.length - 1) {
            posicionActual = 0;
        } else {
            posicionActual++;
        }
        renderizarImagen();
    }

    /**
     * Funcion que cambia la foto en la anterior posicion
     */
    function retrocederFoto() {
        if(posicionActual <= 0) {
            posicionActual = $imagenes.length - 1;
        } else {
            posicionActual--;
        }
        renderizarImagen();
    }

    /**
     * Funcion que actualiza la imagen de imagen dependiendo de posicionActual
     */
    function renderizarImagen() {
        // Ocultar todas las imágenes
        $imagenes.forEach(function(imagen) {
            imagen.style.display = 'none';
        });
        // Mostrar la imagen actual
        $imagenes[posicionActual].style.display = 'block';
    }

    // Eventos
    $botonAvanzar.addEventListener('click', pasarFoto);
    $botonRetroceder.addEventListener('click', retrocederFoto);
    // Iniciar
    renderizarImagen();

    // Iniciar el autoplay
    intervalo = setInterval(pasarFoto, TIEMPO_INTERVALO_MILESIMAS_SEG);
}

