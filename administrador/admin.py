from django.contrib import admin
from .models import Favorito, Tipo_cancha, Cancha, reserva, Disponibilidad, Comentario, ImagenCancha, Region, Direccion, Comuna

class Tipo_canchaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'foto', 'descripcion', 'cantidad_cancha', 'categoria_tipo_cancha')

class CanchaAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_cancha', 'nombre', 'precio', 'capacidad')

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('user', 'cancha', 'fecha', 'horainicio', 'horafin', 'estado')

class DisponibilidadAdmin(admin.ModelAdmin):
    list_display = ('cancha', 'dia_semana', 'horaapertura', 'horacierre')

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('cancha', 'nombre_persona', 'calificacion', 'comentario', 'fecha', 'hora')

class RegionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('cancha', 'user', 'estado')

class DireccionAdmin(admin.ModelAdmin):
    list_display = ('cancha', 'user', 'direccion', 'region', 'comuna')

class ComunaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'region')

class ImagenCanchaAdmin(admin.ModelAdmin):
    list_display = ('cancha', 'imagen')

admin.site.register(Tipo_cancha, Tipo_canchaAdmin)
admin.site.register(Cancha, CanchaAdmin)
admin.site.register(Favorito, FavoritoAdmin)
admin.site.register(reserva, ReservaAdmin)
admin.site.register(Disponibilidad, DisponibilidadAdmin)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(ImagenCancha, ImagenCanchaAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Direccion, DireccionAdmin)
admin.site.register(Comuna, ComunaAdmin)
