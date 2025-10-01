from django.contrib import admin
from .models import CustomUser, Reserva, Habitacion, Hotel, Pago


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'telefono', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'habitacion', 'fecha_inicio', 'fecha_fin', 'estado', 'tipo_pago')
    list_filter = ('estado', 'tipo_pago', 'habitacion__hotel')
    search_fields = ('cliente__username', 'habitacion__numero')


@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'categoria', 'precio', 'hotel')
    list_filter = ('hotel', 'categoria')
    search_fields = ('numero',)


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'administrador')
    search_fields = ('nombre', 'direccion')


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'monto', 'metodo', 'reserva')
    list_filter = ('metodo',)
    search_fields = ('reserva__cliente__username',)
