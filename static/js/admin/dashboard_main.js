function toggleDetails(id) {
    const seccionSresumen = document.getElementById('table_seccion_resumen');
    const allDetails = document.querySelectorAll('.card_details');
    allDetails.forEach(details => {
        if (details.id !== id) {
            details.style.display = 'none';
        }
    });

    const details = document.getElementById(id);
    if (details.style.display === 'none' || details.style.display === '') {
        details.style.display = 'block';
        seccionSresumen.style.display = "none";
    } else {
        details.style.display = 'none';
        seccionSresumen.style.display = "block";
    }

    // Ajustar el desplazamiento si el contenido es mayor
    if (details.style.display === 'block') {
        details.scrollIntoView({ behavior: 'smooth' });
    }
}
