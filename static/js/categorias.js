function filtrarCategorias() {
    const filtro = document.getElementById('filter').value;
    const categorias = document.querySelectorAll('.categoria');

    categorias.forEach(categoria => {
        const deporte = categoria.getAttribute('data-deporte');
        if (filtro === 'todos' || deporte === filtro) {
            categoria.style.display = '';
        } else {
            categoria.style.display = 'none';
        }
    });
}
