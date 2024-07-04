from datetime import datetime, timedelta
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.views.decorators.http import require_POST
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from plantillas.validation.ReservaHoraValidacion import validar_datos_reserva
from administrador.models import Comentario, Comuna, Direccion, Favorito, Region, Tipo_cancha, Cancha, Disponibilidad, reserva, ImagenCancha,Pagos
from geopy.geocoders import Nominatim
import json
from django.conf import settings
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from .forms import SolicitudForm
from decimal import Decimal
from .flow_utils import create_payment,obtener_estado_pago,make_request
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, date, time

# Create your views here.
def index(request):
    # Obtener todas las canchas
    canchas = Cancha.objects.all()

    canchas_con_imagenes = []
    comunas = Comuna.objects.all().order_by('nombre')
    regiones = Region.objects.all().order_by('nombre')
    tipo_canchas = Tipo_cancha.objects.all()

    for cancha in canchas:
        primera_imagen = cancha.imagenes.first()
        direcciones = Direccion.objects.filter(cancha=cancha).values('comuna__nombre', 'region__nombre').first()
        avg_calificacion = Comentario.objects.filter(cancha=cancha).aggregate(Avg('calificacion'))['calificacion__avg']
        es_favorito = False
        if request.user.is_authenticated:
            favorito = Favorito.objects.filter(user=request.user, cancha=cancha).first()
            if favorito:
                es_favorito = favorito.estado
        canchas_con_imagenes.append({
            'cancha': cancha,
            'primera_imagen': primera_imagen,
            'direccion': direcciones,
            'avg_calificacion': avg_calificacion,
            'es_favorito': es_favorito
        })
        print(es_favorito)
    context = {
        "titulo": "Inicio",
        "canchas_con_imagenes": canchas_con_imagenes,
        "regiones": regiones,
        "comunas": comunas,
        "tipo_canchas": tipo_canchas
    }
    return render(request, 'index.html', context)

def buscar_canchas(request):
    query = request.GET.get('q')

    # Obtener todas las canchas
    canchas = Cancha.objects.all()

    # Filtrar las canchas si hay una búsqueda
    if query:
        canchas = canchas.filter(
            Q(nombre__icontains=query) |
            Q(direcciones__comuna__nombre__icontains=query) |
            Q(direcciones__region__nombre__icontains=query) |
            Q(tipo_cancha__nombre__icontains=query)
        ).distinct()

    canchas_con_imagenes = []
    comunas = Comuna.objects.all().order_by('nombre')
    regiones = Region.objects.all().order_by('nombre')
    tipo_canchas = Tipo_cancha.objects.all()

    for cancha in canchas:
        primera_imagen = cancha.imagenes.first()
        direcciones = Direccion.objects.filter(cancha=cancha).values('comuna__nombre', 'region__nombre').first()
        avg_calificacion = Comentario.objects.filter(cancha=cancha).aggregate(Avg('calificacion'))['calificacion__avg']
        es_favorito = False
        if request.user.is_authenticated:
            favorito = Favorito.objects.filter(user=request.user, cancha=cancha).first()
            if favorito:
                es_favorito = favorito.estado
        canchas_con_imagenes.append({
            'cancha': cancha,
            'primera_imagen': primera_imagen,
            'direccion': direcciones,
            'avg_calificacion': avg_calificacion,
            'es_favorito': es_favorito
        })

    context = {
        "titulo": "Buscar Canchas",
        "canchas_con_imagenes": canchas_con_imagenes,
        "regiones": regiones,
        "comunas": comunas,
        "tipo_canchas": tipo_canchas
    }
    return render(request, 'canchas/buscar_canchas.html', context)

@require_POST
def cambiar_favorito(request, id_cancha):
    usuario = request.user
    cancha = get_object_or_404(Cancha, id_cancha=id_cancha)
    favorito, created = Favorito.objects.get_or_create(user=usuario, cancha=cancha)
    if not usuario.is_authenticated:
        return messages.error(request, 'Debes iniciar sesión para agregar a favoritos.')
    # Cambiar el estado de favorito
    favorito.estado = not favorito.estado
    favorito.save()

    return JsonResponse({'success': True, 'favorito': favorito.estado})

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)
    
class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        return super().default(obj)

@login_required
def reservar_hora(request, id_cancha):
    imagenes = ImagenCancha.objects.filter(cancha=id_cancha)
    cancha = get_object_or_404(Cancha, id_cancha=id_cancha)
    disponibilidades = Disponibilidad.objects.filter(cancha=cancha)
    dias_disponibles = [d.dia_semana for d in disponibilidades]

    horas_disponibles = []
    reservas = []
    fecha = None

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')

        validation_result = validar_datos_reserva(fecha, hora_inicio, hora_fin, id_cancha)
        if validation_result['valid']:
            hora_inicio_dt = datetime.strptime(hora_inicio, '%H:%M')
            hora_fin_dt = datetime.strptime(hora_fin, '%H:%M')
            horas_reservadas = (hora_fin_dt - hora_inicio_dt).seconds / 3600
            costo_total = cancha.precio * horas_reservadas
            reserva_temporal= reserva(
                user=request.user,
                cancha_id=id_cancha,
                fecha=fecha,
                horainicio=hora_inicio,
                horafin=hora_fin,
                estado=True,
                total= costo_total
            )
            reserva_temporal.save()
            response= create_payment(request,reserva_temporal.id_reserva  ,costo_total,request.user.email)
            
            print(response)
            try:
                url = response['url']
                token = response['token']
                payment_url = f"{url}?token={token}"
                return redirect(payment_url)
            except KeyError:
                print("ERRORRRR")
        else:
            for error_message in validation_result['errors']:
                messages.error(request, error_message)
                return redirect(f'/reservar_hora/{id_cancha}/')

    if request.method == 'GET' and 'fecha' in request.GET:
        fecha = request.GET.get('fecha')
        
    for disponibilidad in disponibilidades:
        apertura = disponibilidad.horaapertura
        cierre = disponibilidad.horacierre

        reservas_en_fecha = reserva.objects.filter(cancha=cancha, fecha=fecha)

        apertura_datetime = datetime.combine(datetime.today(), apertura)
        cierre_datetime = datetime.combine(datetime.today(), cierre)

        while apertura_datetime <= cierre_datetime:
            hora_actual = apertura_datetime.time()
            siguiente_hora = (apertura_datetime + timedelta(minutes=60)).time()

            if not reservas_en_fecha.filter(Q(horainicio__lte=hora_actual, horafin__gt=hora_actual) | Q(horainicio__lt=siguiente_hora, horafin__gte=siguiente_hora)).exists():
                horas_disponibles.append(hora_actual.strftime("%H:%M"))

            apertura_datetime += timedelta(minutes=60)

    # Serializar reservas
    reservas = list(reserva.objects.filter(cancha=cancha).values())
    for r in reservas:
        r['fecha'] = r['fecha'].strftime("%Y-%m-%d")
        r['horainicio'] = r['horainicio'].strftime("%H:%M")
        r['horafin'] = r['horafin'].strftime("%H:%M")
    reservas_json = json.dumps(reservas, cls=CustomJSONEncoder)

    if len(horas_disponibles) == 0 and fecha is not None:
        dia = datetime.strptime(fecha, "%Y-%m-%d").strftime("%A").lower()
        if dia in dias_disponibles:
            dias_disponibles.remove(dia)


    context = {
        "titulo": "Reservar Hora",
        "cancha": cancha,
        "imagenes": imagenes,
        "disponibilidades": disponibilidades,
        "horas_disponibles": mark_safe(json.dumps(horas_disponibles)),
        "reservas": mark_safe(reservas_json),
        "dias_disponibles": mark_safe(json.dumps(dias_disponibles).lower()),
    }
    print(mark_safe(json.dumps(dias_disponibles).lower()))
    return render(request, 'reservacion/reservar_hora.html', context)



def categoria_cancha(request):
    categorias = Tipo_cancha.objects.all()
    tipos_deportes = Tipo_cancha.objects.values_list('categoria_tipo_cancha', flat=True).distinct()
    
    cantidad_cancha_dict = []
    for categoria in categorias:
        cantidad_cancha = Cancha.objects.filter(tipo_cancha=categoria).count()
        cantidad_cancha_dict.append({'categoria': categoria, 'cantidad': cantidad_cancha})

    context = {
        "titulo": "Categoría de Canchas",
        "categorias": categorias,
        "cantidad_cancha_dict": cantidad_cancha_dict,
        "tipos_deportes": tipos_deportes
    }
    return render(request, 'categorias/categoria_cancha.html', context)

def mas_valorado(request):
    canchas = Cancha.objects.annotate(avg_calificacion=Avg('comentario__calificacion')).filter(avg_calificacion__gte=3).order_by('-avg_calificacion')
    
    canchas_con_imagenes = []
    for cancha in canchas:
        primera_imagen = cancha.imagenes.first()  # Obtén la primera imagen para cada cancha
        canchas_con_imagenes.append({
            'cancha': cancha,
            'primera_imagen': primera_imagen,
        })

    context = {
        "titulo": "Más Valorado",
        "canchas": canchas_con_imagenes,
    }
    return render(request, 'canchas/mas_valorado.html', context)


def detalle_cancha(request, id_cancha):
    cancha = get_object_or_404(Cancha, id_cancha=id_cancha)
    imagenes = cancha.imagenes.all()
    direccion = Direccion.objects.filter(cancha=cancha).first()
    disponibilidad = Disponibilidad.objects.filter(cancha=cancha)

    comentarios = Comentario.objects.filter(cancha=cancha).order_by('-fecha', '-hora')
    avg_calificacion = comentarios.aggregate(Avg('calificacion'))['calificacion__avg'] or 0
    num_comentarios = comentarios.count()
    calificaciones_por_estrella = comentarios.values('calificacion').annotate(count=Count('calificacion')).order_by('-calificacion')
    canchas_recomendadas = Cancha.objects.filter(direcciones__region=direccion.region) \
        .exclude(id_cancha=id_cancha) \
        .annotate(avg_calificacion=Avg('comentario__calificacion')) \
        .filter(avg_calificacion__gte=3) \
        .order_by('-avg_calificacion')[:5]

    location = None
    coords = None
    if direccion:
        geolocator = Nominatim(user_agent="ReservaCancha/0.1", timeout=10)
        address = f"{direccion.direccion}, {direccion.comuna.nombre}, {direccion.region.nombre}, Chile"
        location = geolocator.geocode(address)

    if location:
        coords = f"{location.latitude}, {location.longitude}"
    else:
        messages.error(request, f"Direccion no encontrado porfavor revisa la direcion: {address}")
    comentarios_json = json.dumps([
        {
            'calificacion': comentario.calificacion,
            'comentario': comentario.comentario,
            'nombre_persona': comentario.nombre_persona,
            'fecha': comentario.fecha.isoformat() if comentario.fecha else None,
        } for comentario in comentarios
    ])
    context = {
        "titulo": "Detalle Cancha",
        "cancha": cancha,
        "imagenes": imagenes,
        "disponibilidad": disponibilidad,
        "direccion": direccion,
        "location": location,
        "coords": coords,
        'avg_calificacion': avg_calificacion,
        'num_comentarios': num_comentarios,
        'calificaciones_por_estrella': calificaciones_por_estrella,
        'comentarios': comentarios,
        'comentarios_json': mark_safe(comentarios_json),
        'canchas_recomendadas': canchas_recomendadas,
    }
    return render(request, 'canchas/detalle_cancha.html', context)

def comentario(request, id_cancha):
    if request.method == 'POST':
        cancha = get_object_or_404(Cancha, id_cancha=id_cancha)
        calificacion = request.POST.get('calificacion')
        comentario = request.POST.get('comentario')
        recomendacion = request.POST.get('recomendar') == 'si'
        fecha = datetime.now().date()
        hora = datetime.now().time()

        # Nombre y correo electrónico solo si el usuario no está autenticado
        nombre_persona = request.POST.get('nombre') 
        email = request.POST.get('correo')

        try:
            Comentario.objects.create(
                cancha=cancha,
                nombre_persona=nombre_persona,
                comentario=comentario,
                calificacion=calificacion,
                email=email,
                recomendacion=recomendacion,
                fecha=fecha,
                hora=hora
            )
            messages.success(request, 'Gracias por tu comentario.')
        except Exception as e:
            messages.error(request, 'Error al enviar el comentario. Inténtalo de nuevo más tarde.')

        return redirect('/')

    # Si es un GET, renderizar la página normalmente
    cancha = get_object_or_404(Cancha, id_cancha=id_cancha)
    context = {
        "titulo": "Comentario",
        "cancha": cancha
    }
    return render(request, 'calificacion/comentario.html', context)

# SOLICITUD
def solicitud_empresa(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save()
            return redirect('/')
        else:
            form.add_error(None,"Ocurrio un error, formulario no valido")
    else:
        form= SolicitudForm()
    return render(request,'empresa/solicitud_empresa.html',{'form':form})

def sobre_mi(request):
    usuario = request.user
    context = {
        'titulo': 'Sobre Mi',
        'usuario': usuario,
    }
    return render(request, 'pages/sobre_mi.html', context)

def ayuda(request):
    usuario = request.user

    if request.method == 'POST':
        nombre = request.POST.get('name')
        correo = request.POST.get('email')
        mensaje = request.POST.get('message')

        # Componer el correo
        asunto = f"Solicitud de ayuda de {nombre}"
        mensaje_completo = f"Nombre: {nombre}\nCorreo Electrónico: {correo}\n\nMensaje:\n{mensaje}"
        destinatario = ['i20998785@gmail.com']  # Cambia esto al correo donde deseas recibir los mensajes

        try:
            send_mail(asunto, mensaje_completo, correo, destinatario)
            messages.success(request, 'Tu mensaje ha sido enviado exitosamente.')
        except Exception as e:
            messages.error(request, f'Hubo un problema al enviar el mensaje: {e}')

        return redirect('/')

    context = {
        'titulo': 'Ayuda',
        'usuario': usuario,
    }
    return render(request, 'pages/ayuda.html', context)


# TODOS LOS VIEWS DE LAS HISTORIALES
@login_required
def dashboard_historial(request):
    usuario = request.user
    reservas = reserva.objects.filter(user=usuario).order_by('fecha')
    
    fechas_reservas = []
    for reserva_item in reservas:
        fecha = reserva_item.fecha
        if fecha not in fechas_reservas:
            fechas_reservas.append(fecha)

    context = {
        'titulo': 'Historial',
        'usuario': usuario,
        'fechas_reservas': fechas_reservas,
        'reservas': reservas,
    }
    return render(request, 'historial/historial.html', context)


@login_required
def dashboard_historial_administrar(request, id_cancha):
    usuario = request.user
    try:
        cancha = Cancha.objects.get(id_cancha=id_cancha)
    except Cancha.DoesNotExist:
        # Manejar el caso cuando no se encuentra la cancha
        return render(request, 'error.html', {'mensaje': 'La cancha no existe'})

    today = datetime.today()
    day_of_comprar = today.day
    direcciones = cancha.direcciones.all() 
    disponibilidades = Disponibilidad.objects.filter(cancha=cancha)
    estado_reservas = reserva.objects.filter(cancha=cancha).values('estado')
    context = {
        'titulo': 'Administrar Historial',
        'usuario': usuario,
        'day_of_comprar': day_of_comprar,
        'cancha': cancha,
        'disponibilidades': disponibilidades,
        'direcciones': direcciones,
        'estado_reservas': estado_reservas,
    }
    return render(request, 'historial/administrar_historial.html', context)
# FIN TODOS LOS VIEWS DE LAS HISTORIALES


# VIEWS DE LAS COMUNICACION

@login_required
def dashboard_comunicacion(request, id_cancha):
    usuario = request.user
    cancha = get_object_or_404(Cancha, id_cancha=id_cancha)
    nombre_usuario = usuario.first_name + "-" + cancha.user.first_name

    if request.method == 'POST':
        mensaje = request.POST.get('enviarmensajes')
        archivo = request.FILES.get('enviarfile')

        cancha = get_object_or_404(Cancha, id_cancha=id_cancha)
        email_destinatario = cancha.user.email
        email_remitente = usuario.email
        
        # Crear el objeto EmailMessage
        email = EmailMessage(
            'Asunto del correo electrónico',
            mensaje,
            email_remitente,  # Email del remitente
            [email_destinatario],  # Lista de destinatarios
        )

        # Adjuntar el archivo al correo electrónico
        email.attach(archivo.name, archivo.read(), archivo.content_type)

        # Enviar el correo electrónico
        email.send()

        messages.success(request, 'Mensaje enviado exitosamente')
        return redirect('plantillas:dashboard_historial_administrar', id_cancha=id_cancha)

    context = {
        'titulo': 'Comunicaciónes  con ' + usuario.first_name,
        'usuario': usuario,
        'cancha': cancha,
        'nombre_usuario': nombre_usuario,
    }
    return render(request, 'comunicacion/comunicacion.html', context)

def termino_uso(request):
    context = {
        'titulo': 'Terminos de uso',
    }
    return render(request, 'pages/terminos_uso.html', context)

def politica_privacidad(request):
    context = {
        'titulo': 'Politica de privacidad',
    }
    return render(request, 'pages/politica_privacidad.html', context)


@login_required
def dashboard_favorita(request):
    usuario = request.user
    canchas_con_imagenes = []

    # Obtener las canchas que son favoritas del usuario
    favoritos = Favorito.objects.filter(user=usuario, estado=True)
    canchas = [favorito.cancha for favorito in favoritos]

    for cancha in canchas:
        primera_imagen = cancha.imagenes.first()
        avg_calificacion = Comentario.objects.filter(cancha=cancha).aggregate(Avg('calificacion'))['calificacion__avg']
        canchas_con_imagenes.append({
            'cancha': cancha,
            'primera_imagen': primera_imagen,
            'avg_calificacion': avg_calificacion
        })

    context = {
        'titulo': 'Favoritos',
        'usuario': usuario,
        'canchas_con_imagenes': canchas_con_imagenes,
    }
    return render(request, 'pages/favoritas.html', context)


@csrf_exempt
def retorno_flow(request):
    token = request.POST.get('token')
    url = 'https://sandbox.flow.cl/api/payment/getStatus'
    parametros = {
        'apiKey': settings.FLOW_KEY_SANDBOX,
        'token': token
    }
    response= make_request(url, parametros, method='GET')
    transaccion={
        'commerceOrder': response['commerceOrder'],
        'requestDate': response['requestDate'],
        'subject': response['subject'],
        'payer': response['payer'],
        'amount': response['amount'],
        'currency': response['currency'],
        'media': response['paymentData']['media'],
        'status': response['status']
    }
    orden_comercio = transaccion['commerceOrder']
    numero_reserva= int(orden_comercio[1:])
    reserva1= reserva.objects.get(id_reserva= numero_reserva)
    if transaccion['status'] == 2:
        reserva1.estado_pago = "Pagado"
        reserva1.save()
        usuario_cancha= reserva1.cancha.user
        pago = reserva1.total * Decimal('0.8')
        nuevo_pago=Pagos(
            usuario_empresa=usuario_cancha,
            reserva= reserva1,
            total_pago= pago
        )
        nuevo_pago.save()

    else:
        reserva1.delete()
    
    return render(request,'retorno_flow.html',{'transaccion': transaccion})

