from django.shortcuts import get_object_or_404
from administrador.models import Cancha, reserva
from datetime import datetime

def validar_datos_cancha(nombre, precio, imagenes, descripcion, subdescripcion, ubicacion, tipo, capacidad, hora_inicio, hora_fin):
    validation_result = {'valid': True, 'errors': {}}

    # Validar campos vacíos
    if not nombre or nombre == "":
        validation_result['valid'] = False
        validation_result['errors']['nombre'] = 'El nombre es obligatorio.'
    if not precio or precio == "":
        validation_result['valid'] = False
        validation_result['errors']['precio'] = 'El precio es obligatorio.'
    if not imagenes:
        validation_result['valid'] = False
        validation_result['errors']['imagenes'] = 'Se debe seleccionar al menos una imagen.'
    if not descripcion or descripcion == "":
        validation_result['valid'] = False
        validation_result['errors']['descripcion'] = 'La descripción es obligatoria.'
    if not subdescripcion or subdescripcion == "":
        validation_result['valid'] = False
        validation_result['errors']['subdescripcion'] = 'La subdescripción es obligatoria.'
    if not ubicacion or ubicacion == "":
        validation_result['valid'] = False
        validation_result['errors']['ubicacion'] = 'La ubicación es obligatoria.'
    if not tipo or tipo == "":
        validation_result['valid'] = False
        validation_result['errors']['tipo'] = 'El tipo es obligatorio.'
    if not capacidad or capacidad == "":
        validation_result['valid'] = False
        validation_result['errors']['capacidad'] = 'La capacidad es obligatoria.'
    if not hora_inicio or hora_inicio == "":
        validation_result['valid'] = False
        validation_result['errors']['hora_inicio'] = 'La hora de inicio es obligatoria.'
    if not hora_fin or hora_fin == "":
        validation_result['valid'] = False
        validation_result['errors']['hora_fin'] = 'La hora de fin es obligatoria.'

    # Agregar otras validaciones necesarias, como longitud de campos, formatos válidos, etc.

    return validation_result
