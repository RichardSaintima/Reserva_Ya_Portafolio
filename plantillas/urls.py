from django.urls import path
from . import views

app_name = 'plantillas'

urlpatterns = [
    path('', views.index, name='index'),
    path('reservar_hora/<int:id_cancha>/', views.reservar_hora, name='reservar_hora'),
    path('categoria_cancha/', views.categoria_cancha, name='categoria_cancha'),
    path('buscar_canchas/', views.buscar_canchas, name='buscar_canchas'),
    path('detalle_cancha/<int:id_cancha>/', views.detalle_cancha, name='detalle_cancha'),
    path('mas_valorado/', views.mas_valorado, name='mas_valorado'),
    path('comentario/<int:id_cancha>/', views.comentario, name='comentario'),
    path('solicitud_empresa/',views.solicitud_empresa, name= 'solicitud_empresa'),
    path('sobre_mi/', views.sobre_mi, name='sobre_mi'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('cambiar_favorito/<int:id_cancha>/', views.cambiar_favorito, name='cambiar_favorito'),
    path('dashboard_historial/', views.dashboard_historial, name='dashboard_historial'),
    path('dashboard_historial/adminitrar/<int:id_cancha>/', views.dashboard_historial_administrar, name='dashboard_historial_administrar'),
    path('dashboard_comunicacion/<int:id_cancha>/', views.dashboard_comunicacion, name='dashboard_comunicacion'),
    path('termino_uso/', views.termino_uso, name='termino_uso'),
    path('politica_privacidad/', views.politica_privacidad, name='politica_privacidad'),
    path('retorno_flow/', views.retorno_flow, name='retorno_flow'),
    path('dashboard_favorita/', views.dashboard_favorita, name='dashboard_favorita'),
]
