from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('landing/', views.landing, name='landing'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('registro/', views.registro, name='registro'), 
    path('home_cliente/', views.home_cliente, name='home_cliente'),
    path('adminrf_home/', views.adminrf_home, name='adminrf_home'),
    path('adminrf/habitaciones/', views.adminrf_habitacion_list, name='adminrf_habitacion_list'),
    path('adminrf/habitaciones/nueva/', views.adminrf_habitacion_create, name='adminrf_habitacion_create'),
    path('adminrf/habitaciones/editar/<int:pk>/', views.adminrf_habitacion_update, name='adminrf_habitacion_update'),
    path('adminrf/habitaciones/eliminar/<int:pk>/', views.adminrf_habitacion_delete, name='adminrf_habitacion_delete'),
    path('adminrf/clientes/', views.adminrf_cliente_list, name='adminrf_cliente_list'),
    path('adminrf/clientes/nuevo/', views.adminrf_cliente_create, name='adminrf_cliente_create'),
    path('adminrf/clientes/editar/<int:pk>/', views.adminrf_cliente_update, name='adminrf_cliente_update'),
    path('adminrf/clientes/eliminar/<int:pk>/', views.adminrf_cliente_delete, name='adminrf_cliente_delete'),
    path('adminrf/reservas/', views.adminrf_reserva_list, name='adminrf_reserva_list'),
    path('adminrf/reservas/nueva/', views.adminrf_reserva_create, name='adminrf_reserva_create'),
    path('adminrf/reservas/editar/<int:pk>/', views.adminrf_reserva_update, name='adminrf_reserva_update'),
    path('adminrf/reservas/eliminar/<int:pk>/', views.adminrf_reserva_delete, name='adminrf_reserva_delete'),
    path('adminrf/empleados/', views.adminrf_empleado_list, name='adminrf_empleado_list'),
    path('adminrf/empleados/nuevo/', views.adminrf_empleado_create, name='adminrf_empleado_create'),
    path('adminrf/empleados/editar/<int:pk>/', views.adminrf_empleado_update, name='adminrf_empleado_update'),
    path('adminrf/empleados/eliminar/<int:pk>/', views.adminrf_empleado_delete, name='adminrf_empleado_delete'),
    path('cliente_home/', views.cliente_home, name='cliente_home'),
    path('historial_reservas/', views.historial_reservas, name='historial_reservas'),
    path('reserva_habitacion/', views.reserva_habitacion, name='reserva_habitacion'),
    path('cliente_datos/', views.cliente_datos, name='cliente_datos'),
    path('home_cliente/', views.home_cliente, name='home_cliente'),
    path('procesar_reserva/', views.procesar_reserva, name='procesar_reserva'),
    path('habitaciones/', views.lista_habitaciones, name='lista_habitaciones'),
    path('habitacion/<int:habitacion_id>/', views.detalle_habitacion, name='detalle_habitacion'),
    path('reserva/<int:habitacion_id>/', views.reserva_habitacion, name='reserva_habitacion'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)