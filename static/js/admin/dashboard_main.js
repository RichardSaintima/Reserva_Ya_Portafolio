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

document.addEventListener('DOMContentLoaded', function() {
    const btnOpen = document.getElementById('btnDashboardMenuMobile');
    const btnClose = document.getElementById('btnDashboardCloseMenuMobile');
    const sidebar = document.getElementById('dashboardSidebar');

    btnOpen.addEventListener('click', function() {
        sidebar.classList.toggle('open');
        btnOpen.style.display = sidebar.classList.contains('open') ? 'none' : 'block';
        btnClose.style.display = sidebar.classList.contains('open') ? 'block' : 'none';
    });
    
    btnClose.addEventListener('click', function() {
        sidebar.classList.toggle('open');
        btnOpen.style.display = sidebar.classList.contains('open') ? 'none' : 'block';
        btnClose.style.display = sidebar.classList.contains('open') ? 'block' : 'none';
    });
  });