from django.db import models
from django.contrib.auth.models import User

class Administrador(models.Model):
    admin_nombre = models.CharField(max_length=100)
    admin_apellidos = models.CharField(max_length=100)
    admin_email = models.EmailField(max_length=150)
    admin_telefono = models.CharField(max_length=15)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.admin_nombre} {self.admin_apellidos}'

class Cliente(models.Model):
    cliente_nombre = models.CharField(max_length=100)
    cliente_apellidos = models.CharField(max_length=100)
    cliente_email = models.EmailField(max_length=150)
    cliente_telefono = models.CharField(max_length=15)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'{self.cliente_nombre} {self.cliente_apellidos}'

class Empleado(models.Model):
    empleado_nombre = models.CharField(max_length=100)
    empleado_apellidos = models.CharField(max_length=100)
    empleado_rol = models.CharField(max_length=50)
    empleado_email = models.EmailField(max_length=150)
    empleado_telefono = models.CharField(max_length=15)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.empleado_nombre} {self.empleado_apellidos}'

class Hotel(models.Model):
    hotel_nombre = models.CharField(max_length=100)
    hotel_direccion = models.CharField(max_length=255)
    
    def __str__(self):
        return self.hotel_nombre

class Habitacion(models.Model):
    habitacion_numero = models.CharField(max_length=10)
    habitacion_categoria = models.CharField(max_length=50)
    habitacion_descripcion = models.TextField(null=True, blank=True)
    habitacion_precio = models.DecimalField(max_digits=10, decimal_places=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    habitacion_imagen = models.ImageField(upload_to='img/habitaciones/', null=True, blank=True)  # Campo para la imagen

    def __str__(self):
        return f'Habitación {self.habitacion_numero} - {self.hotel.hotel_nombre}'

class Reserva(models.Model):
    reserva_fecha = models.DateField(auto_now_add=True)  # Fecha cuando se realizó la reserva
    reserva_fecha_inicio = models.DateField()  # Fecha de inicio de la estancia
    reserva_fecha_fin = models.DateField()  # Fecha de finalización de la estancia
    reserva_total_dias = models.IntegerField(blank=True, null=True)  # Se puede calcular automáticamente
    reserva_estado = models.CharField(max_length=50, default='Pendiente')  # Estado de la reserva
    # tipo_pago = models.CharField(max_length=50)  # Tipo de pago seleccionado (tarjeta, PayPal, etc.)
    tipo_pago = models.CharField(max_length=100, default='Tarjeta de Crédito')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con Cliente
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)  # Relación con Habitación

    def __str__(self):
        return f'Reserva de {self.cliente} en {self.habitacion}'

    # Sobrescribimos el método save para calcular los días automáticamente
    def save(self, *args, **kwargs):
        if self.reserva_fecha_inicio and self.reserva_fecha_fin:
            self.reserva_total_dias = (self.reserva_fecha_fin - self.reserva_fecha_inicio).days
        super(Reserva, self).save(*args, **kwargs)

# class Reserva(models.Model):
#     reserva_fecha = models.DateField()
#     reserva_fecha_inicio = models.DateField()
#     reserva_fecha_fin = models.DateField()
#     reserva_total_dias = models.IntegerField()
#     reserva_estado = models.CharField(max_length=50)
#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
#     habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'Reserva de {self.cliente} en {self.habitacion}'

class Pago(models.Model):
    pago_fecha = models.DateField()
    pago_monto = models.DecimalField(max_digits=10, decimal_places=2)
    pago_metodo = models.CharField(max_length=50)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Pago de {self.pago_monto} para {self.reserva}'

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Usuario(models.Model):
    usuario_nombre = models.CharField(max_length=100)
    usuario_contrasena = models.CharField(max_length=128)
    usuario_tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario_nombre
