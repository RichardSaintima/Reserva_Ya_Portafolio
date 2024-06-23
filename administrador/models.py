from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.utils import timezone


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