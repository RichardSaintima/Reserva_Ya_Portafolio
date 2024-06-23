from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Rol(models.Model):
    id_rol= models.AutoField(primary_key=True)
    tipo_rol= models.CharField(max_length=30)

    def __str__(self):
        return self.tipo_rol

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Usuario')
    rol= models.ForeignKey(Rol, on_delete=models.CASCADE,default=1)

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'

    def __str__(self):
        return self.user.username  
     
def create_user_profile(sender, instance, created, **kwargs):
    if created and isinstance(instance, User):
        Profile.objects.create(user=instance)
    
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

post_save.connect(create_user_profile)
post_save.connect(save_user_profile,sender=User)

class Solicitud(models.Model):
    id_solicitud= models.AutoField(primary_key=True)
    rut_empresa= models.CharField(max_length=12)
    nombre_empresa= models.CharField(max_length=100)
    razon_social= models.CharField(max_length=100)
    direccion_empresa=models.CharField(max_length=150)
    estado= models.CharField(default='pendiente',max_length=20)
    correo_electronico= models.CharField(max_length=40)

    def __str__(self):
        return self.nombre_empresa
