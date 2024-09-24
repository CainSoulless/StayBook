from django.contrib import admin
from .models import Hotel, Habitacion

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['hotel_nombre', 'hotel_direccion']

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ['habitacion_numero', 'habitacion_categoria', 'habitacion_precio']