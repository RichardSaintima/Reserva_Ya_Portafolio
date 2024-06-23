document.addEventListener("DOMContentLoaded", function() {
  var lastScrollTop = 0;
  var header = document.getElementById("mostrar");
  // Evento que se ejecuta cuando se hace scroll en la página
  window.addEventListener("scroll", function() {
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    // Si el scroll es menor a 100px, muestra el header normalmente
    if (scrollTop > lastScrollTop) {
      // Si el scroll es hacia abajo, oculta el header
      header.style.top = "-100px";
      // Desactiva los eventos del mouse sobre el header
      header.style.pointerEvents = "none"; 
    } else {
      // Si el scroll es hacia arriba, muestra el header
      header.style.top = "0";
      // Re-activa los eventos del mouse sobre el header
      header.style.pointerEvents = "auto"; 
    }
    lastScrollTop = scrollTop;
  });
});
