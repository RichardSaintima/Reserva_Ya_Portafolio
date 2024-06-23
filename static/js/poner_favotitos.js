document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.like-button').forEach(button => {
      button.addEventListener('click', function(e) {
          e.preventDefault();
          const url = this.getAttribute('data-url');
          const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

          fetch(url, {
              method: 'POST',
              headers: {
                  'X-CSRFToken': csrftoken,
                  'Content-Type': 'application/json'
              }
          })
          .then(response => {
              if (!response.ok) {
                  throw new Error('Network response was not ok');
              }
              return response.json();
          })
          .then(data => {
              if (data.success) {
                  const heartIcon = this.querySelector('i.fa');
                  if (data.favorito) {
                      heartIcon.classList.remove('fa-heart-crack');
                      heartIcon.classList.add('fa-heart');
                  } else {
                      heartIcon.classList.remove('fa-heart');
                      heartIcon.classList.add('fa-heart-crack');
                  }
              }
          })
          .catch(error => {
              console.error('There was a problem with the fetch operation:', error);
          });
      });
  });
  document.querySelectorAll('.sacarFovirotos').forEach(button => {
    button.addEventListener('click', function() {
      fetch(this.getAttribute('data-url'), {
        method: 'POST', // O el método adecuado para tu solicitud
        headers: {
          'X-CSRFToken': getCookie('csrftoken') // Asegúrate de tener esta función para obtener el token CSRF
        }
      }).then(response => {
        if (response.ok) {
          // Recargar la página después de que se haya completado la solicitud
          location.reload();
        } else {
          console.error('Error al sacar de favoritos');
        }
      });
    });
  });
  
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (const element of cookies) {
        const cookie = element.trim();
        // Busca el nombre de la cookie especificada
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  

});
