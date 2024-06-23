document.addEventListener('DOMContentLoaded', function() {
    const activarBtn = document.getElementById('activarBtn');
    const desactivarBtn = document.getElementById('desactivarBtn');

    if (activarBtn && desactivarBtn) {
        activarBtn.addEventListener('click', function(event) {
            event.preventDefault();
            activarBtn.style.display = 'none';
            desactivarBtn.style.display = 'inline-block';
        });

        desactivarBtn.addEventListener('click', function(event) {
            event.preventDefault();
            desactivarBtn.style.display = 'none';
            activarBtn.style.display = 'inline-block';
        });
    }

});
