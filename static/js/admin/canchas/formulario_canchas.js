document.addEventListener('DOMContentLoaded', function() {
    const imagenesInput = document.getElementById('imagenes');
    const mostrarImagenesSeleccionado = document.getElementById('mostrarImagenesSeleccionado');
    const imagenesEliminadasInput = document.getElementById('imagenesEliminadas');

    let imagenesExistentes = Array.from(document.querySelectorAll('.existing_image img')).map(img => img.src);
    let imagenesNuevas = [];

    imagenesInput.addEventListener('change', function() {
        const files = Array.from(this.files);
        imagenesNuevas = imagenesNuevas.concat(files);
        mostrarImagenes();
    });

    function eliminarImagenExistente(index) {
        const imgSrc = imagenesExistentes[index];
        imagenesExistentes.splice(index, 1);
        actualizarImagenesEliminadas(imgSrc);
        mostrarImagenes();
    }
    function asignarEventosEliminar() {
        const botonesEliminar = document.querySelectorAll('.btn-eliminar');
        botonesEliminar.forEach(boton => {
            boton.addEventListener('click', function() {
                const parentDiv = this.parentNode;
                const index = parseInt(parentDiv.getAttribute('data-index'));
                eliminarImagenExistente(index);
            });
        });
    }

    asignarEventosEliminar();
    function eliminarImagenNueva(index) {
        imagenesNuevas.splice(index, 1);
        mostrarImagenes();
    }

    function actualizarImagenesEliminadas(imgSrc) {
        const eliminadas = imagenesEliminadasInput.value ? imagenesEliminadasInput.value.split(',') : [];
        eliminadas.push(imgSrc);
        imagenesEliminadasInput.value = eliminadas.join(',');
    }

    function mostrarImagenes() {
        mostrarImagenesSeleccionado.innerHTML = '';

        imagenesExistentes.forEach((src, index) => {
            const imageDiv = document.createElement('div');
            imageDiv.classList.add('existing_image');
            imageDiv.innerHTML = `
                <img src="${src}" alt="Imagen existente">
                <button type="button" onclick="eliminarImagenExistente(${index})">X</button>
            `;
            mostrarImagenesSeleccionado.appendChild(imageDiv);
        });

        imagenesNuevas.forEach((file, index) => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imageDiv = document.createElement('div');
                imageDiv.classList.add('new_image');
                imageDiv.innerHTML = `
                    <img src="${e.target.result}" alt="Imagen seleccionada">
                    <button type="button" onclick="eliminarImagenNueva(${index})">X</button>
                `;
                mostrarImagenesSeleccionado.appendChild(imageDiv);
            };
            reader.readAsDataURL(file);
        });
    }

    mostrarImagenes();

    window.eliminarImagenExistente = eliminarImagenExistente;
    window.eliminarImagenNueva = eliminarImagenNueva;

    const regionSelect = document.getElementById('region');
    const comunaSelect = document.getElementById('comuna');
    const comunas = JSON.parse('{{ comunas_json|escapejs }}');

    regionSelect.addEventListener('change', function() {
        const regionId = this.value;
        comunaSelect.innerHTML = '<option value="" selected disabled>-- Seleccionar comuna --</option>';
        comunas.forEach(comuna => {
            if (comuna.region_id == regionId) {
                const option = document.createElement('option');
                option.value = comuna.id;
                option.textContent = comuna.nombre;
                comunaSelect.appendChild(option);
            }
        });
    });
});

function agregarAgenda(disponibilidadOpciones, diaSeleccionado = null, horaInicio = null, horaFin = null, idx) {
    const container = document.getElementById('disponibilidad_container');
    const div = document.createElement('div');
    div.className = 'disponibilidad_item';

    const select = document.createElement('select');
    select.name = 'disponibilidad_dia';
    select.onchange = function() {
        toggleTimeInputs(this.value, div, idx);
    };

    const defaultOption = document.createElement('option');
    defaultOption.text = 'Seleccione un día';
    defaultOption.value = '';
    defaultOption.selected = true;
    defaultOption.disabled = true;
    select.add(defaultOption);

    disponibilidadOpciones.forEach(option => {
        const dia = option[0];
        const valor = option[1];
        const opt = document.createElement('option');
        opt.value = valor;
        opt.text = dia;
        if (diaSeleccionado && diaSeleccionado === dia) {
            opt.selected = true;
        }
        select.add(opt);
    });

    const eliminarBtn = document.createElement('button');
    eliminarBtn.className = 'eliminar_agenda_btn';
    eliminarBtn.innerHTML = '&#128465;';
    eliminarBtn.onclick = function() {
        container.removeChild(div);
    };

    const selectContainer = document.createElement('div');
    selectContainer.style.display = 'flex';
    selectContainer.style.alignItems = 'center';
    selectContainer.appendChild(select);
    selectContainer.appendChild(eliminarBtn);

    div.appendChild(selectContainer);
    container.appendChild(div);

    if (diaSeleccionado && horaInicio && horaFin) {
        toggleTimeInputs(diaSeleccionado, div, idx, horaInicio, horaFin);
    }
}

function toggleTimeInputs(valor, container, idx, horaInicio = null, horaFin = null) {
    let timeInputs = container.querySelector('.time_inputs');
    if (!timeInputs) {
        timeInputs = document.createElement('div');
        timeInputs.className = 'time_inputs';

        const horaInicioInput = document.createElement('input');
        horaInicioInput.type = 'time';
        horaInicioInput.name = `hora_inicio_${idx}`;
        horaInicioInput.required = true;
        horaInicioInput.style.marginRight = '10px';
        if (horaInicio) {
            horaInicioInput.value = horaInicio;
        }

        const horaFinInput = document.createElement('input');
        horaFinInput.type = 'time';
        horaFinInput.name = `hora_fin_${idx}`;
        horaFinInput.required = true;
        if (horaFin) {
            horaFinInput.value = horaFin;
        }

        timeInputs.appendChild(horaInicioInput);
        timeInputs.appendChild(horaFinInput);
        container.appendChild(timeInputs);
    } else {
        timeInputs.style.display = 'block';
    }
}
