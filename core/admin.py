from django.contrib import admin
from .models import Cliente, Empleado, Reserva, Habitacion, Hotel, Pago

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente_nombre', 'cliente_apellidos', 'cliente_email', 'cliente_telefono')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('empleado_nombre', 'empleado_apellidos', 'empleado_rol', 'empleado_email', 'empleado_telefono')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'habitacion', 'reserva_fecha_inicio', 'reserva_fecha_fin', 'reserva_estado')

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('habitacion_numero', 'habitacion_categoria', 'habitacion_precio', 'hotel')

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotel_nombre', 'hotel_direccion')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('pago_fecha', 'pago_monto', 'pago_metodo', 'reserva')

# @admin.register(Usuario)
# class UsuarioAdmin(admin.ModelAdmin):
#     list_display = ('usuario_nombre', 'usuario_contrasena', 'usuario_tipo')
#     list_filter = ('usuario_tipo',)
#     search_fields = ('usuario_nombre', 'usuario_tipo')
