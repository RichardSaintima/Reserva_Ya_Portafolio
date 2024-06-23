from django.urls import path
from . import views

app_name = 'administrador'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard_usuario/administrar', views.dashboard_usuario_administrar, name='dashboard_usuario_administrar'),
    path('dashboard_cancha/administrar', views.dashboard_detalle_cancha, name='dashboard_detalle_cancha'),
 
    path('dashboard_cancha/', views.dashboard_cancha, name='dashboard_cancha'),
    path('dashboard_cancha/agregar', views.dashboard_cancha_agregar, name='dashboard_cancha_agregar'),
    path('dashboard_cancha/modificar/<int:id_cancha>/', views.dashboard_cancha_modificar, name='dashboard_cancha_modificar'),
    path('dashboard/dashboard_cancha/administrar/<int:id_cancha>/', views.dashboard_cancha_administrar, name='dashboard_cancha_administrar'),
    path('dashboard_cancha_eliminar/<int:id_cancha>/', views.dashboard_cancha_eliminar, name='dashboard_cancha_eliminar'),
    
    path('dashboard_informe/', views.dashboard_informe, name='dashboard_informe'),
    
    path('dashboard_ordenes/', views.dashboard_ordenes, name='dashboard_ordenes'),
    path('dashboard_orden/administrar/<int:id_reserva>/', views.dashboard_orden_administrar, name='dashboard_orden_administrar'),
    
    path('buscar_administrador/', views.buscar_administrador, name='buscar_administrador'),
    
    path('dashboard_configuracion/', views.dashboard_configuracion, name='dashboard_configuracion'),
    
    path('dashboard_perfil/', views.dashboard_perfil, name='dashboard_perfil'),
    path('dashboard_perfil/modificar', views.dashboard_perfil_modificar, name='dashboard_perfil_modificar'),


    path('dashboard_solicitudes/', views.dashboard_solicitudes, name='dashboard_solicitudes'),
    path('dashboard_solicitudes/aceptar/<int:id_solicitud>',views.dashboard_aceptar_solicitud,name='dashboard_aceptar_solicitud')
]
