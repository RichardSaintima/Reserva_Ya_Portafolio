from django.shortcuts import get_object_or_404
from administrador.models import Cancha, reserva
from datetime import datetime

def validar_datos_reserva(fecha, hora_inicio, hora_fin, id_cancha):
    validation_result = {'valid': True, 'errors': []}
    # Validar campos vacíos
    if not fecha or fecha == "":
        validation_result['valid'] = False
        validation_result['errors'].append('La fecha esta vacia.')
    if not hora_inicio or hora_inicio == "":
        validation_result['valid'] = False
        validation_result['errors'].append('La hora de inicio esta vacia.')
    if not hora_fin or hora_fin == "":
        validation_result['valid'] = False
        validation_result['errors'].append( 'La hora de fin esta vacia.')
    
    cancha = get_object_or_404(Cancha, id_cancha=id_cancha)
    reservas = reserva.objects.filter(cancha=cancha, fecha=fecha)

    # Convertir a objetos datetime para facilitar la comparación
    hora_inicio = datetime.strptime(hora_inicio, '%H:%M').time()
    hora_fin = datetime.strptime(hora_fin, '%H:%M').time()

    for reserva_item in reservas:
        if (hora_inicio < reserva_item.horafin and hora_fin > reserva_item.horainicio):
            validation_result['valid'] = False
            validation_result['errors'].append("La cancha ya está reservada para el rango de horas seleccionado.")

    # Si todo es correcto, retorna True y ningún error
    return validation_result
