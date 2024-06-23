document.addEventListener('DOMContentLoaded', () => {
    const usuario = document.getElementById('usuario');
    const usuarioMovil = document.getElementById('usuarioMovil');
    const barraUsuario = document.getElementById('barraUsuario');
    const barraUsuarioMovil = document.getElementById('barraUsuarioMovil');
    const btnMenuMobile = document.getElementById('btnMenuMobile');
    const btnCloseMenuMobile = document.getElementById('btnCloseMenuMobile');
    const menuMobile = document.getElementById('menuMobile');
  
    window.addEventListener('scroll', function() {
      // Oculta los menús al hacer scroll
      barraUsuario.classList.remove('show');
      barraUsuarioMovil.classList.remove('mostrarUsuarioMovil');
      menuMobile.style.display = 'none';
      btnMenuMobile.style.display = 'block';
      btnCloseMenuMobile.style.display = 'none';
    });
  
    usuario.addEventListener('click', (event) => {
      event.preventDefault();
      barraUsuario.classList.toggle('show');
    });
  
    usuarioMovil.addEventListener('click', (event) => {
      event.preventDefault();
      barraUsuarioMovil.classList.toggle('mostrarUsuarioMovil');
    });
  
    btnMenuMobile.addEventListener('click', () => {
      menuMobile.style.display = 'block';
      btnMenuMobile.style.display = 'none';
      btnCloseMenuMobile.style.display = 'block';
    });
  
    btnCloseMenuMobile.addEventListener('click', () => {
      menuMobile.style.display = 'none';
      btnMenuMobile.style.display = 'block';
      btnCloseMenuMobile.style.display = 'none';
    });
  });
  