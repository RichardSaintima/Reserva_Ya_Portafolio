from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from celery import shared_task

class Tipo_cancha(models.Model):
    id_tipo_cancha = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='img/categorias/')
    descripcion = models.TextField()
    cantidad_cancha = models.IntegerField()
    categoria_tipo_cancha = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
    
class Cancha(models.Model):
    id_cancha = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_cancha = models.ForeignKey('Tipo_cancha', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=210, null=True, blank=True)
    subdescripcion = models.CharField(max_length=210, null=True, blank=True)
    capacidad = models.IntegerField()
    precio = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre} {self.user} {self.id_cancha} {self.tipo_cancha} {self.precio} {self.descripcion} {self.subdescripcion} {self.capacidad}"


class Favorito(models.Model):
    id_favorito = models.AutoField(primary_key=True)
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    estado = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cancha} {self.user} {self.estado}"

class ImagenCancha(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='img/canchas/')

#para historial de reservas 
class reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User model
    cancha = models.ForeignKey('Cancha', on_delete=models.CASCADE , null=True)  # ForeignKey to Cancha model
    fecha = models.DateField()
    horainicio = models.TimeField()
    horafin = models.TimeField()
    estado = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    estado_pago= models.CharField(max_length=10,default='Pendiente')
    fecha_creacion= models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.id_reserva} {self.user} {self.cancha} {self.fecha} {self.horainicio} {self.horafin} {self.estado}"
    
    
class Comentario(models.Model):
    id_comentario = models.AutoField(primary_key=True)
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    nombre_persona = models.CharField(max_length=100, null=True, blank=True)
    comentario = models.TextField()
    calificacion = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    recomendacion = models.BooleanField(null=True, blank=True)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"{self.cancha} {self.fecha} {self.hora} {self.calificacion} {self.recomendacion} {self.comentario} {self.email} {self.nombre_persona}"

class Region(models.Model):
    id_region = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre    
    
class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='direcciones')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=100)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user} {self.direccion} {self.cancha} {self.comuna} {self.region}"

class Disponibilidad(models.Model):
    DIAS_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]

    id_disponibilidad = models.AutoField(primary_key=True)
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=10, choices=DIAS_SEMANA)
    horaapertura = models.TimeField()
    horacierre = models.TimeField()

    def __str__(self):
        return f"{self.cancha.nombre} - {self.dia_semana} ({self.horaapertura} - {self.horacierre})"
    
@shared_task
def eliminar_objetos_pendientes():
    tiempo_limite = timezone.now() - timedelta(minutes=1)
    objetos_pendientes = reserva.objects.filter(estado="Pendiente", fecha_creacion__lte=tiempo_limite)
    objetos_pendientes.delete()

class Banco(models.Model):
    id_banco= models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=100)
    codigo= models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class DatosTransferencia(models.Model):
    id_datos_transferencia= models.AutoField(primary_key=True)
    usuario= models.ForeignKey(User, on_delete=models.CASCADE)
    banco= models.ForeignKey(Banco,on_delete=models.CASCADE)
    nombre= models.CharField(max_length=100)
    numero_cuenta= models.CharField(max_length=20)
    rut = models.CharField(max_length=12)
    TIPO_CUENTA_CHOICES=[
        ('corriente', 'Cuenta Corriente'),
        ('ahorro', 'Cuenta de Ahorro'),
        ('vista', 'Cuenta Vista'),
        ('cuenta_rut', 'Cuenta RUT'),
        ('ahorro_vivienda', 'Cuenta de Ahorro para la Vivienda'),
    ]
    tipo_cuenta= models.CharField(max_length=30,choices=TIPO_CUENTA_CHOICES)
    correo= models.EmailField(blank=True,null=True)

    def __str__(self):
        return f"Transferencia a {self.nombre} en {self.banco.nombre}"
    
class Pagos(models.Model):
    id_pagos= models.AutoField(primary_key=True)
    usuario_empresa= models.ForeignKey(User,on_delete=models.CASCADE)
    estado_pago= models.CharField(max_length=100,default="No transferido")
    reserva= models.ForeignKey(reserva,on_delete=models.CASCADE)
    total_pago= models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    fecha = models.DateTimeField(default=timezone.now)
    foto_comprobante=  models.ImageField(upload_to='img/comprobantes/', blank=True, null=True)

    def __str__(self):
        return f"Pago a {self.usuario_empresa.username} estado: {self.estado_pago}"