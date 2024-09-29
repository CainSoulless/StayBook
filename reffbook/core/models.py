from django.db import models

'''class Usuario(models.Model):        -------> MODIFICAR USUARIO
    USUARIO_TIPOS = [
        ('cliente', 'Cliente'),
        ('empleado', 'Empleado'),
        ('administrador', 'Administrador'),
    ]
    
    usuario_nombre = models.CharField(max_length=50)
    usuario_email = models.EmailField(max_length=150, unique=True)
    usuario_contrasena = models.CharField(max_length=100)
    usuario_tipo = models.CharField(max_length=15, choices=USUARIO_TIPOS, default='cliente')
    
    def __str__(self):
        return f'{self.usuario_nombre} ({self.get_usuario_tipo_display()})' '''

class Administrador(models.Model):
    admin_nombre = models.CharField(max_length=100)
    admin_apellidos = models.CharField(max_length=100)
    admin_email = models.EmailField(max_length=150)
    admin_telefono = models.CharField(max_length=15)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.admin_nombre} {self.admin_apellidos}'

class Cliente(models.Model):
    cliente_nombre = models.CharField(max_length=100)
    cliente_apellidos = models.CharField(max_length=100)
    cliente_email = models.EmailField(max_length=150)
    cliente_telefono = models.CharField(max_length=15)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'{self.cliente_nombre} {self.cliente_apellidos}'

class Empleado(models.Model):
    empleado_nombre = models.CharField(max_length=100)
    empleado_apellidos = models.CharField(max_length=100)
    empleado_rol = models.CharField(max_length=50)
    empleado_email = models.EmailField(max_length=150)
    empleado_telefono = models.CharField(max_length=15)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
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
    
    def __str__(self):
        return f'Habitación {self.habitacion_numero} - {self.hotel.hotel_nombre}'

class Reserva(models.Model):
    reserva_fecha = models.DateField()
    reserva_fecha_inicio = models.DateField()
    reserva_fecha_fin = models.DateField()
    reserva_total_dias = models.IntegerField()
    reserva_estado = models.CharField(max_length=50)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)

    def __str__(self):
        return f'Reserva de {self.cliente} en {self.habitacion}'

class Pago(models.Model):
    pago_fecha = models.DateField()
    pago_monto = models.DecimalField(max_digits=10, decimal_places=2)
    pago_metodo = models.CharField(max_length=50)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Pago de {self.pago_monto} para {self.reserva}'
