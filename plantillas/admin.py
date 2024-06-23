from django.contrib import admin
from .models import Rol, Solicitud, Profile
# Register your models here.

class RolAdmin(admin.ModelAdmin):
    list_display= ('id_rol', 'tipo_rol')

admin.site.register(Rol,RolAdmin)

class SolicitudAdmin(admin.ModelAdmin):
    list_display= ('id_solicitud','rut_empresa','nombre_empresa','razon_social','direccion_empresa','estado','correo_electronico')

admin.site.register(Solicitud,SolicitudAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','rol')
admin.site.register(Profile,ProfileAdmin)
