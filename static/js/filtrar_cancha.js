function filtrarPorTipoLasCanchas() {
    const filtroTipo = document.getElementById('tipo').value;
    const filtroRegion = document.getElementById('region').value;
    const filtroComuna = document.getElementById('comuna').value;
    const filtroPrecio = parseFloat(document.getElementById('precio').value);

    const canchas = document.querySelectorAll('.parafiltro');

    canchas.forEach(cancha => {
        const region = cancha.getAttribute('data-region');
        const comuna = cancha.getAttribute('data-comuna');
        const precio = parseFloat(cancha.getAttribute('data-precio'));
        const tipo = cancha.getAttribute('data-tipo');

        const filtrarPorTipo = filtroTipo === '0' || filtroTipo === tipo;
        const filtrarPorRegion = filtroRegion === '0' || filtroRegion === region;
        const filtrarPorComuna = filtroComuna === '0' || filtroComuna === comuna;
        const filtrarPorPrecio = isNaN(filtroPrecio) || precio <= filtroPrecio;
        
        const mostrar = filtrarPorTipo && filtrarPorRegion && filtrarPorComuna && filtrarPorPrecio;
        console.log(filtrarPorTipo, filtrarPorRegion, filtrarPorComuna, filtrarPorPrecio);
        console.log(mostrar);
        cancha.style.display = mostrar ? '' : 'none';
    });
}

document.getElementById('tipo').addEventListener('change', filtrarPorTipoLasCanchas);
document.getElementById('region').addEventListener('change', filtrarPorTipoLasCanchas);
document.getElementById('comuna').addEventListener('change', filtrarPorTipoLasCanchas);
document.getElementById('precio').addEventListener('input', filtrarPorTipoLasCanchas);


function mostrarOpcion() {
    // Obtener el valor seleccionado
    let seleccion = document.getElementById("filtrar").value;
    
    // Ocultar todos los divs
    let divs = document.querySelectorAll('.contenidofiltrarCanchas div');
    divs.forEach(function(div) {
        div.style.display = 'none';
    });
    
    // Mostrar solo el div correspondiente a la opción seleccionada
    if (seleccion !== '0') {
        let divMostrar = document.querySelector('.contenidofiltrarCanchas .' + seleccion);
        divMostrar.style.display = 'block';
    }
}
