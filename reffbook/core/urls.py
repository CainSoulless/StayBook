from django.urls import path
from . import views

urlpatterns = [
    path('landing/', views.landing, name='landing'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('registro/', views.registro, name='registro'), 
    path('home_cliente/', views.home_cliente, name='home_cliente'),
    path('admin/', views.admin_home, name='admin_home'),
    path('admin/habitaciones/', views.admin_habitacion_list, name='admin_habitacion_list'),
    path('admin/habitaciones/nueva/', views.admin_habitacion_create, name='admin_habitacion_create'),
    path('admin/habitaciones/editar/<int:pk>/', views.admin_habitacion_update, name='admin_habitacion_update'),
    path('admin/habitaciones/eliminar/<int:pk>/', views.admin_habitacion_delete, name='admin_habitacion_delete'),
    path('admin/clientes/', views.admin_cliente_list, name='admin_cliente_list'),
    path('admin/clientes/nuevo/', views.admin_cliente_create, name='admin_cliente_create'),
    path('admin/clientes/editar/<int:pk>/', views.admin_cliente_update, name='admin_cliente_update'),
    path('admin/clientes/eliminar/<int:pk>/', views.admin_cliente_delete, name='admin_cliente_delete'),
    path('admin/reservas/', views.admin_reserva_list, name='admin_reserva_list'),
    path('admin/reservas/nueva/', views.admin_reserva_create, name='admin_reserva_create'),
    path('admin/reservas/editar/<int:pk>/', views.admin_reserva_update, name='admin_reserva_update'),
    path('admin/reservas/eliminar/<int:pk>/', views.admin_reserva_delete, name='admin_reserva_delete'),
    path('admin/empleados/', views.admin_empleado_list, name='admin_empleado_list'),
    path('admin/empleados/nuevo/', views.admin_empleado_create, name='admin_empleado_create'),
    path('admin/empleados/editar/<int:pk>/', views.admin_empleado_update, name='admin_empleado_update'),
    path('admin/empleados/eliminar/<int:pk>/', views.admin_empleado_delete, name='admin_empleado_delete'),
]
