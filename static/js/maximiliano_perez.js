document.addEventListener('DOMContentLoaded', function() {
    const verMasBtns = document.querySelectorAll('.ver-mas'); // Selecciona todos los botones 'Ver más'
    const descripciones = document.querySelectorAll('.descripcion-actividad'); // Selecciona todas las descripciones

    verMasBtns.forEach((btn, index) => {
        const descripcion = descripciones[index];

        // Función para verificar la altura del elemento
        function verificarAltura() {
            if (descripcion.offsetHeight > parseInt(window.getComputedStyle(descripcion).lineHeight) * 2) {
                btn.style.display = 'block'; // Muestra el botón si el contenido tiene más de dos líneas
            } else {
                btn.style.display = 'none'; // Oculta el botón si el contenido tiene dos líneas o menos
            }
        }

        // Verificar la altura al cargar la página
        verificarAltura();

        // Evento clic en el botón "Ver más"
        btn.addEventListener('click', function() {
            descripcion.classList.toggle('expandida');
            if (descripcion.classList.contains('expandida')) {
                btn.textContent = 'Ver menos';
            } else {
                btn.textContent = 'Ver más';
            }
        });
    });
});

    let comentariosIniciales = 3;
    let comentariosVisibles = comentariosIniciales;

    function mostrarMasComentarios() {
        let comentariosDiv = document.getElementById('comentarios');
        let verMasButton = document.getElementById('verMasComentarios');
        let verMenosButton = document.getElementById('verMenosComentarios');

        for (let i = comentariosVisibles; i < comentarios.length; i++) {
            let comentarioHTML = `
                <div class="comentario">
                    <div>
                        <div>
                            <p>
                                ${Array.from({length: 5}, (_, j) => j < comentarios[i].calificacion ? '<i class="fa-solid fa-star" style="color: #f7b500;"></i>' : '<i class="fa-solid fa-star" style="color: #0790f88e;"></i>').join('')}
                            </p>
                        </div>
                        <p>${comentarios[i].comentario}</p>
                    </div>
                    <div>
                        <p><strong>${comentarios[i].nombre_persona}</strong></p>
                        <p>Enviado <span>${comentarios[i].fecha}</span></p>
                    </div>
                </div>`;
            comentariosDiv.innerHTML += comentarioHTML;
        }

        comentariosVisibles = comentarios.length;
        verMasButton.style.display = 'none';
        verMenosButton.style.display = 'block';
    }

    function mostrarMenosComentarios() {
        let comentariosDiv = document.getElementById('comentarios');
        let verMasButton = document.getElementById('verMasComentarios');
        let verMenosButton = document.getElementById('verMenosComentarios');

        comentariosDiv.innerHTML = '';
        for (let i = 0; i < comentariosIniciales; i++) {
            let comentarioHTML = `
                <div class="comentario">
                    <div>
                        <div>
                            <p>
                                ${Array.from({length: 5}, (_, j) => j < comentarios[i].calificacion ? '<i class="fa-solid fa-star" style="color: #f7b500;"></i>' : '<i class="fa-solid fa-star" style="color: #0790f88e;"></i>').join('')}
                            </p>
                        </div>
                        <p>${comentarios[i].comentario}</p>
                    </div>
                    <div>
                        <p><strong>${comentarios[i].nombre_persona}</strong></p>
                        <p>Enviado <span>${comentarios[i].fecha}</span></p>
                    </div>
                </div>`;
            comentariosDiv.innerHTML += comentarioHTML;
        }

        comentariosVisibles = comentariosIniciales;
        verMasButton.style.display = 'block';
        verMenosButton.style.display = 'none';
    }

    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.like-btn').forEach(function(btn) {
            btn.addEventListener('click', function() {
                sendLikeDislike(btn, 'like');
            });
        });
    
        document.querySelectorAll('.dislike-btn').forEach(function(btn) {
            btn.addEventListener('click', function() {
                sendLikeDislike(btn, 'dislike');
            });
        });
    });
    
    function sendLikeDislike(btn, action) {
        const commentId = btn.closest('.likes').getAttribute('data-comment-id');
        const formData = new FormData();
        formData.append('action', action);
    
        fetch(`/like_dislike/${commentId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error al enviar la solicitud.');
            }
        })
        .then(data => {
            // Actualizar el contador de likes o dislikes en la interfaz
            document.querySelector(`.like-count-${commentId}`).textContent = data.likes;
            document.querySelector(`.dislike-count-${commentId}`).textContent = data.dislikes;
    
            // Agregar o quitar la clase 'liked' o 'disliked' según corresponda
            btn.classList.toggle('liked', data.action === 'like');
            btn.classList.toggle('disliked', data.action === 'dislike');
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    document.addEventListener('DOMContentLoaded', function () {
        const rutInput = document.querySelector('input[name="rut_empresa"]');
        
        rutInput.addEventListener('input', function (e) {
            let value = e.target.value.replace(/[^\dKk]/g, ''); // Solo permite dígitos y la letra 'K' en minúscula o mayúscula
            
            // Formatea el RUT con puntos y guión
            if (value.length > 1) {
                value = value.slice(0, value.length - 1) + '-' + value.slice(value.length - 1);
            }
            if (value.length > 5) {
                value = value.slice(0, value.length - 5) + '.' + value.slice(value.length - 5);
            }
            if (value.length > 9) {
                value = value.slice(0, value.length - 9) + '.' + value.slice(value.length - 9);
            }
            
            e.target.value = value.toUpperCase(); // Convierte todo a mayúsculas antes de asignarlo al input
        });
    });
        