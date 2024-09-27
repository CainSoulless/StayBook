from django.urls import path
from . import views

urlpatterns = [
    path('landing/', views.landing, name='landing'),
    path('habitaciones/', views.habitacion_list, name='habitacion_list'),
    path('habitaciones/nueva/', views.habitacion_create, name='habitacion_create'),
    path('habitaciones/editar/<int:pk>/', views.habitacion_update, name='habitacion_update'),
    path('habitaciones/eliminar/<int:pk>/', views.habitacion_delete, name='habitacion_delete'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('registro/', views.registro, name='registro'), 
    path('home_cliente/', views.home_cliente, name='home_cliente'),
]
