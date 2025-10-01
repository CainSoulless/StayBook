from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('cliente', 'Cliente'),
        ('empleado', 'Empleado'),
        ('administrador', 'Administrador'),
    )
    role = models.CharField(max_length=20, choices=USER_TYPES, default='cliente')
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Hotel(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='hoteles/logos/', blank=True, null=True)
    correo_contacto = models.EmailField(blank=True, null=True)
    administrador = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="hotel_admin",
        limit_choices_to={'role': 'administrador'},
        null=True, blank=True
    )

    def __str__(self):
        return self.nombre


class Habitacion(models.Model):
    numero = models.CharField(max_length=10)
    categoria = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="habitaciones")
    imagen = models.ImageField(upload_to='img/habitaciones/', null=True, blank=True)

    def __str__(self):
        return f'Habitación {self.numero} - {self.hotel.nombre}'


class Reserva(models.Model):
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_dias = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=50, default='Pendiente')
    tipo_pago = models.CharField(max_length=100, default='Tarjeta de Crédito')
    cliente = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'cliente'}
    )
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)

    def __str__(self):
        return f'Reserva de {self.cliente.username} en {self.habitacion}'

    def save(self, *args, **kwargs):
        if self.fecha_inicio and self.fecha_fin:
            self.total_dias = (self.fecha_fin - self.fecha_inicio).days
        super().save(*args, **kwargs)


class Pago(models.Model):
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=50)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name="pagos")

    def __str__(self):
        return f'Pago {self.monto} para {self.reserva}'
