import calendar
import os
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Avg, Count
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Favorito, Tipo_cancha, Cancha, ImagenCancha, Disponibilidad, reserva, Comentario, Region, Direccion, Comuna
from django.db import transaction
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Sum
from django.core.mail import send_mail
from plantillas.models import Solicitud, Rol

# Create your views here.

# TODOS LOS VIEWS DE DASHBOARD
@login_required
def dashboard(request):
    usuario = request.user
    canchas = Cancha.objects.all()
    reservas = reserva.objects.filter(cancha__in=canchas)
    cantidad_canchas = canchas.count()
    usuarios = User.objects.all().count()
    users = User.objects.all()
    # Calcular la suma de los precios de todas las reservas
    total_precios_reservas = reservas.aggregate(total=Sum('cancha__precio'))['total']
    today = date.today()
    ventas_mensuales = []
    for i in range(5, -1, -1):
        first_day_of_month = today.replace(day=1, month=today.month - i)
        last_day_of_month = today.replace(day=calendar.monthrange(today.year, today.month - i)[1], month=today.month - i)
        ventas_mes = reservas.filter(fecha__range=[first_day_of_month, last_day_of_month]).aggregate(total=Sum('cancha__precio'))['total']
        ventas_mensuales.append(ventas_mes or 0)
    context = {
        'titulo': 'DashBoard',
        'usuario': usuario,
        'ventas_mensuales': ventas_mensuales,
        'reservas': reservas,
        'canchas': canchas,
        'usuarios': usuarios,
        'users': users,
        'cantidad_canchas': cantidad_canchas,
        'total_precios_reservas': total_precios_reservas,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def buscar_administrador(request):
    usuario = request.user
    query = request.GET.get('q', '')

    # Filtrar canchas y reservas relacionadas con las canchas del usuario
    canchas = Cancha.objects.filter(user=usuario)
    reservas = reserva.objects.filter(cancha__in=canchas)
    usuarios = User.objects.all()
    
    if query:
        canchas = canchas.filter(
            Q(nombre__icontains=query) |
            Q(direcciones__comuna__nombre__icontains=query) |
            Q(direcciones__region__nombre__icontains=query) |
            Q(tipo_cancha__nombre__icontains=query)
        ).distinct()

        reservas = reservas.filter(
            Q(cancha__nombre__icontains=query) |
            Q(cancha__direcciones__comuna__nombre__icontains=query) |
            Q(cancha__direcciones__region__nombre__icontains=query)
        ).distinct()

        usuarios = usuarios.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)|
            Q(first_name__icontains=query)|
            Q(last_name__icontains=query)
        ).distinct()

    context = {
        'titulo': 'Buscar Administrador',
        'usuario': usuario,
        'canchas': canchas,
        'reservas': reservas,
        'usuarios': usuarios,
        'query': query,
    }
    return render(request, 'pages/buscar_administrador.html', context)

@login_required
def dashboard_usuario_administrar(request):
    usuario = request.user
    context = {
        'titulo': 'Administar Usuario',
        'usuario': usuario,
    }
    return render(request, 'dashboard/detalle_usuario/administar_usuario.html', context)

@login_required
def dashboard_orden_administrar(request, id_reserva):
    usuario = request.user
    reserva_obj = get_object_or_404(reserva, id_reserva=id_reserva)
    cancha_obj = reserva_obj.cancha
    reservas = reserva.objects.filter(cancha=cancha_obj)
    direcciones = Direccion.objects.filter(cancha=cancha_obj) 
    

    context = {
        'titulo': 'Administrar Orden',
        'usuario': usuario,
        'reservas': reservas,
        'cancha': cancha_obj,
        "direcciones": direcciones,
    }
    return render(request, 'ordenes/administar_orden.html', context)

@login_required
def dashboard_ordenes(request):
    usuario = request.user
    # Obtener todas las canchas del usuario
    canchas_usuario = Cancha.objects.filter(user=usuario)
    # Obtener todas las reservas en las canchas del usuario
    reservas = reserva.objects.filter(cancha__in=canchas_usuario)
    # Obtener todas las direcciones relacionadas con las reservas
    direcciones = Direccion.objects.filter(cancha__in=reservas.values_list('cancha', flat=True))

    context = {
        'titulo': 'Administrar Ordenes detalles',
        'usuario': usuario,
        'reservas': reservas,
        'canchas_usuario': canchas_usuario,
        'direcciones': direcciones,
    }
    return render(request, 'ordenes/detalles_nuevas_ordenes.html', context)



@login_required
def dashboard_detalle_cancha(request):
    usuario = request.user
    context = {
        'titulo': 'Administar Cancha',
        'usuario': usuario,
    }
    return render(request, 'dashboard/detalle_cancha/administrar_detalle_Tipo_cancha.html', context)

# FIN DE LOS VIEWS DE DASHBOARD


# TODOS LOS VIEWS DE LAS CANCHAS
@login_required
def dashboard_cancha(request):
    canchas = Cancha.objects.filter(user=request.user)
    context = {
        'titulo': 'Cancha Administrador',
        'canchas': canchas
    }
    return render(request, 'canchas/canchas.html', context)


@login_required
def dashboard_cancha_agregar(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        imagenes = request.FILES.getlist('imagenes')
        descripcion = request.POST.get('descripcion')
        subdescripcion = request.POST.get('subdescripcion')
        ubicacion = request.POST.get('ubicacion')
        tipo = request.POST.get('tipo')
        capacidad = request.POST.get('capacidad')
        dias = request.POST.getlist('disponibilidad_dia')
        horas_inicio = [request.POST.get(f'hora_inicio_{idx}') for idx, _ in enumerate(dias)]
        horas_fin = [request.POST.get(f'hora_fin_{idx}') for idx, _ in enumerate(dias)]

        if not nombre or not precio or not imagenes or not descripcion or not tipo or not capacidad or not dias:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('administrador:dashboard_cancha_agregar')

        try:
            tipo_cancha = Tipo_cancha.objects.get(id_tipo_cancha=tipo)
        except Tipo_cancha.DoesNotExist:
            messages.error(request, 'El tipo de cancha seleccionado no existe.')
            return redirect('administrador:dashboard_cancha_agregar')

        with transaction.atomic():
            cancha = Cancha.objects.create(
                nombre=nombre,
                precio=precio,
                descripcion=descripcion,
                subdescripcion=subdescripcion,
                capacidad=capacidad,
                tipo_cancha=tipo_cancha,
                user=request.user
            )
            Direccion.objects.create(
                cancha=cancha,
                user=request.user,
                direccion=ubicacion,
                comuna_id=request.POST.get('comuna'),
                region_id=request.POST.get('region')
            )

            for imagen in imagenes:
                ImagenCancha.objects.create(cancha=cancha, imagen=imagen)

            for dia, inicio, fin in zip(dias, horas_inicio, horas_fin):
                if inicio and fin:
                    Disponibilidad.objects.create(
                        cancha=cancha,
                        dia_semana=dia,
                        horaapertura=inicio,
                        horacierre=fin
                    )
                else:
                    messages.error(request, f'Debe ingresar las horas de inicio y fin para el día {dia.capitalize()}.')

            messages.success(request, 'Cancha agregada correctamente.')
            return redirect('administrador:dashboard_cancha')
    else:
        tipos_cancha = Tipo_cancha.objects.all()
        comunas = Comuna.objects.all().order_by('nombre')
        regiones = Region.objects.all().order_by('nombre')
        disponibilidad_opciones = Disponibilidad.DIAS_SEMANA
        disponibilidad_opciones_json = json.dumps(list(Disponibilidad.DIAS_SEMANA))
        
        context = {
            'tipos_cancha': tipos_cancha,
            'titulo': 'Agregar Cancha',
            'comunas': comunas,
            'regiones': regiones,
            'disponibilidad_opciones': disponibilidad_opciones,
            'disponibilidad_opciones_json': disponibilidad_opciones_json,
            'disponibilidades_existentes_json': json.dumps([]),  # Lista vacía para agregar
        }
        return render(request, 'canchas/agregar_canchas.html', context)




@login_required
def dashboard_cancha_modificar(request, id_cancha):
    cancha = get_object_or_404(Cancha, id_cancha=id_cancha, user=request.user)
    comunas = Comuna.objects.all().order_by('nombre')
    regiones = Region.objects.all().order_by('nombre')
    disponibilidades_existentes = cancha.disponibilidad_set.all()

    if request.method == "POST":
        # Obtener los valores de los campos del formulario
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        descripcion = request.POST.get('descripcion')
        subdescripcion = request.POST.get('subdescripcion')
        ubicacion = request.POST.get('ubicacion')
        tipo = request.POST.get('tipo')
        capacidad = request.POST.get('capacidad')
        comuna_id = request.POST.get('comuna')
        region_id = request.POST.get('region')
        dias = request.POST.getlist('disponibilidad_dia')
        horas_inicio = [request.POST.get(f'hora_inicio_{idx}') for idx, _ in enumerate(dias)]
        horas_fin = [request.POST.get(f'hora_fin_{idx}') for idx, _ in enumerate(dias)]
        imagenesEliminadas = request.POST.get('imagenesEliminadas', '').split(',')
        
        # Verificar que todos los campos obligatorios estén presentes
        if not nombre or not precio or not descripcion:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('administrador:dashboard_cancha_modificar', id_cancha=id_cancha)

        # Actualizar la cancha
        cancha.nombre = nombre
        cancha.precio = precio
        cancha.descripcion = descripcion
        cancha.subdescripcion = subdescripcion
        cancha.capacidad = capacidad
        cancha.tipo_cancha_id = tipo
        cancha.save()

        # Actualizar la dirección de la cancha
        comuna = get_object_or_404(Comuna, pk=comuna_id)
        region = get_object_or_404(Region, pk=region_id)
        direccion = cancha.direcciones.first()

        if direccion:
            direccion.direccion = ubicacion
            direccion.comuna = comuna
            direccion.region = region
            direccion.save()
        else:
            Direccion.objects.create(cancha=cancha, user=request.user, direccion=ubicacion, comuna=comuna, region=region)

        # Eliminar las imágenes y disponibilidades que ya no son necesarias
        for img_url in imagenesEliminadas:
            imagen_obj = cancha.imagenes.filter(imagen=img_url).first()
            if imagen_obj:
                imagen_obj.delete()

        for disponibilidad in disponibilidades_existentes:
            if disponibilidad.dia_semana not in dias:
                disponibilidad.delete()

        # Agregar las nuevas imágenes y disponibilidades
        for imagen_file in request.FILES.getlist('imagenes'):
            ImagenCancha.objects.create(cancha=cancha, imagen=imagen_file)

        for dia, inicio, fin in zip(dias, horas_inicio, horas_fin):
            if inicio and fin:
                # Verificar si ya existe una disponibilidad para el mismo día
                disponibilidad_existente = Disponibilidad.objects.filter(cancha=cancha, dia_semana=dia).first()
                if disponibilidad_existente:
                    # Si existe, actualiza las horas de inicio y fin
                    disponibilidad_existente.horaapertura = inicio
                    disponibilidad_existente.horacierre = fin
                    disponibilidad_existente.save()
                else:
                    # Si no existe, crea una nueva disponibilidad
                    Disponibilidad.objects.create(cancha=cancha, dia_semana=dia, horaapertura=inicio, horacierre=fin)
            else:
                messages.error(request, f'Debe ingresar las horas de inicio y fin para el día {dia.capitalize()}.')

        messages.success(request, 'Cancha modificada correctamente.')
        return redirect('administrador:dashboard_cancha')

    tipos_cancha = Tipo_cancha.objects.all()
    disponibilidades_existentes = list(disponibilidades_existentes.values('id_disponibilidad', 'dia_semana', 'horaapertura', 'horacierre'))
    for disponibilidad in disponibilidades_existentes:
        disponibilidad['horaapertura'] = disponibilidad['horaapertura'].strftime('%H:%M')
        disponibilidad['horacierre'] = disponibilidad['horacierre'].strftime('%H:%M')

    disponibilidades_existentes_json = json.dumps(disponibilidades_existentes).lower()
    disponibilidad_opciones = Disponibilidad.DIAS_SEMANA
    disponibilidad_opciones_json = json.dumps(list(Disponibilidad.DIAS_SEMANA))

    comunas_json = json.dumps(list(comunas.values('id_comuna', 'nombre', 'region_id')))

    # Asegúrate de definir la variable direccion para la solicitud GET
    direccion = cancha.direcciones.first()

    context = {
        'titulo': 'Modificar Cancha',
        'cancha': cancha,
        'tipos_cancha': tipos_cancha,
        'direccion': direccion,
        'comunas': comunas,
        'regiones': regiones,
        'disponibilidades_existentes_json': disponibilidades_existentes_json,
        'disponibilidad_opciones': disponibilidad_opciones,
        'disponibilidad_opciones_json': disponibilidad_opciones_json,
        'comunas_json': comunas_json,
    }
    return render(request, 'canchas/modificar_canchas.html', context)


@login_required
def dashboard_cancha_administrar(request, id_cancha):
    cancha = get_object_or_404(Cancha, id_cancha=id_cancha, user=request.user)
    imagenes = cancha.imagenes.all()  # Obtener imágenes relacionadas con la cancha
    direcciones = cancha.direcciones.all()  # Obtener direcciones relacionadas con la cancha
    disponibilidades = Disponibilidad.objects.filter(cancha=cancha)  # Obtener disponibilidad de la cancha
    
    context = {
        'titulo': 'Administar Cancha',
        'cancha': cancha,
        'imagenes': imagenes,
        'direcciones': direcciones,
        'disponibilidades': disponibilidades
    }
    return render(request, 'canchas/administrar_cancha.html', context)


@login_required
def dashboard_cancha_eliminar(request, id_cancha):
    cancha = get_object_or_404(Cancha, id_cancha=id_cancha, user=request.user)
    disponibilidad = Disponibilidad.objects.filter(cancha=cancha)
    # Eliminar las imágenes asociadas
    for imagen in cancha.imagenes.all():
        imagen.imagen.delete()
    # Eliminar las disponibilidades asociadas
    disponibilidad.delete()
    cancha.delete()
    messages.success(request, 'Cancha eliminada correctamente.')
    return redirect('administrador:dashboard_cancha')

# FIN TODOS LOS VIEWS DE LAS CANCHAS


# TODOS LOS VIEWS DE LAS INFORMES
@login_required
def dashboard_informe(request):
    usuario = request.user
    today = datetime.today()
    day_of_month = today.day
    canchas = Cancha.objects.filter(user=usuario)
    reservas = reserva.objects.filter(cancha__in=canchas)
    cantidad_canchas = canchas.count()
    
    # Calcular la suma de los precios de todas las reservas
    total_precios_reservas = reservas.aggregate(total=Sum('cancha__precio'))['total'] or 0

    # Datos diarios para el mes actual
    ventas_diarias = [0] * day_of_month
    ordenes_diarias = [0] * day_of_month
    for i in range(day_of_month):
        day_start = today.replace(day=i+1)
        day_end = day_start + timedelta(days=1)
        ventas_dia = reservas.filter(fecha__range=[day_start, day_end]).aggregate(total=Sum('cancha__precio'))['total'] or 0
        ordenes_dia = reservas.filter(fecha__range=[day_start, day_end]).count()
        ventas_diarias[i] = ventas_dia
        ordenes_diarias[i] = ordenes_dia

    # Datos mensuales para los últimos 6 meses
    ventas_mensuales = [0] * 6
    ordenes_mensuales = [0] * 6
    for i in range(6):
        start_date = (today.replace(day=1) - timedelta(days=i*30)).replace(day=1)
        end_date = start_date + timedelta(days=calendar.monthrange(start_date.year, start_date.month)[1] - 1)
        ventas_mes = reservas.filter(fecha__range=[start_date, end_date]).aggregate(total=Sum('cancha__precio'))['total'] or 0
        ordenes_mes = reservas.filter(fecha__range=[start_date, end_date]).count()
        ventas_mensuales[-(i+1)] = ventas_mes
        ordenes_mensuales[-(i+1)] = ordenes_mes

    # Calcular canchas por mes
    canchas_por_mes = []
    for i in range(1, 13):
        canchas_por_mes.append(Cancha.objects.filter(created_at__month=i).count())

    context = {
        'titulo': 'Informe',
        'usuario': usuario,
        'cancha_data': canchas_por_mes,
        'ventas_data': ventas_diarias,  # Datos diarios
        'orden_data': ordenes_diarias,  # Datos diarios
        'ventas_mensuales': ventas_mensuales,  # Datos mensuales
        'ordenes_mensuales': ordenes_mensuales,  # Datos mensuales
        'day_of_month': day_of_month,
        'cantidad_canchas': cantidad_canchas,
        'reservas': reservas.count(),  # Usar .count() aquí para obtener el total de reservas
        'total_precios_reservas': total_precios_reservas,
    }
    return render(request, 'informes/informe.html', context)
# FIN TODOS LOS VIEWS DE LAS INFORMES



# TODOS LOS VIEWS DE LAS HISTORIALES
@login_required
def dashboard_perfil(request):
    usuario = request.user
    
    context = {
        'titulo': 'Perfil',
        'usuario': usuario,
    }
    return render(request, 'perfil/perfil.html', context)

@login_required
def dashboard_perfil_modificar(request):
    usuario = request.user
    
    context = {
        'titulo': 'Modificar Historial',
        'usuario': usuario,
    }
    return render(request, 'perfil/administrar_perfil.html', context)

@login_required
def dashboard_configuracion(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada exitosamente.')
        return redirect('/')
    usuario = request.user
    context = {
        'titulo': 'Configuración',
        'usuario': usuario,
    }
    return render(request, 'perfil/configuracion_cuenta.html', context)
# FIN TODOS LOS VIEWS DE LAS HISTORIALES

# VIEWS DE SOLICITUDES
@login_required
def dashboard_solicitudes(request):
    solicitudes = Solicitud.objects.all()
    return render(request,'solicitud/solicitudes.html',{'solicitudes':solicitudes})

@login_required
def dashboard_aceptar_solicitud(request,id_solicitud):
    solicitud= get_object_or_404(Solicitud,id_solicitud= id_solicitud)
    nueva_empresa= User.objects.create_user(
        username = solicitud.nombre_empresa,
        email = solicitud.correo_electronico,
        password= solicitud.rut_empresa
    )
    nueva_empresa.save()
    solicitud.estado = "Aceptada"
    solicitud.save()
        # Obtener el perfil del usuario recién creado
    perfil_empresa = nueva_empresa.profile
    # Obtener el objeto Rol con id 2
    rol = Rol.objects.get(pk=2)

    # Cambiar la propiedad 'rol' del perfil
    perfil_empresa.rol = rol

    # Guardar los cambios en el perfil
    perfil_empresa.save()

    mensaje= "Tu solicitud de la creacion de una cuenta de empresa a sido aceptada!\nTus Credenciales son las siguientes: \n"+"Username: "+solicitud.nombre_empresa+"\nPassword: "+solicitud.rut_empresa+"\nRecuerda que para subir tus espacios debes agregar tus datos de transferencia!\nSaludos"

    send_mail("Creacion de cuenta de empresa",mensaje,settings.EMAIL_HOST_USER,[solicitud.correo_electronico] )
    return render(request,'solicitud/solicitudes.html')