import os
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


# --------------------------
# CustomUser
# --------------------------
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('cliente', 'Cliente'),
        ('empleado', 'Empleado'),
        ('administrador', 'Administrador'),
    )
    role = models.CharField(max_length=20, choices=USER_TYPES, default='cliente')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    hotel = models.ForeignKey(
        'Hotel', on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios'
    )

    def save(self, *args, **kwargs):
        # Si el usuario es superusuario, forzamos su rol a 'administrador'
        if self.is_superuser:
            self.role = 'administrador'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# --------------------------
# Función para nombrar el logo del hotel
# --------------------------
def hotel_logo_upload_path(instance, filename):
    """
    Genera una ruta y nombre de archivo único y seguro para el logo del hotel.
    Ejemplo: hoteles/logos/logo-hotel-las-palmas_9be44c1e.png
    """
    ext = filename.split('.')[-1]
    safe_name = slugify(instance.nombre or "hotel")
    new_filename = f"logo_{safe_name}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('hoteles', 'logos', new_filename)


# --------------------------
# Hotel
# --------------------------
class Hotel(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to=hotel_logo_upload_path, blank=True, null=True)
    correo_contacto = models.EmailField(blank=True, null=True)
    color_primario = models.CharField(max_length=20, default="#0c3a4d")
    color_secundario = models.CharField(max_length=20, default="#e7b10a")
    subdominio = models.CharField(max_length=50, unique=True, null=True, blank=True)
    administrador = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="hotel_admin",
        limit_choices_to={'role': 'administrador'},
        null=True, blank=True
    )

    def __str__(self):
        return self.nombre or "Hotel sin nombre"

    def save(self, *args, **kwargs):
        """
        Elimina el logo anterior si se reemplaza.
        """
        try:
            old_instance = Hotel.objects.get(pk=self.pk)
            if old_instance.logo and old_instance.logo != self.logo:
                old_instance.logo.delete(save=False)
        except Hotel.DoesNotExist:
            pass
        super().save(*args, **kwargs)


# --------------------------
# Habitacion
# --------------------------
class Habitacion(models.Model):
    numero = models.CharField(max_length=10)
    categoria = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="habitaciones")
    imagen = models.ImageField(upload_to='img/habitaciones/', null=True, blank=True)

    def __str__(self):
        return f'Habitación {self.numero} - {self.hotel.nombre}'


# --------------------------
# Reserva
# --------------------------
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

    @property
    def hotel(self):
        return self.habitacion.hotel


# --------------------------
# Pago
# --------------------------
class Pago(models.Model):
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=50)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name="pagos")

    def __str__(self):
        return f'Pago {self.monto} para {self.reserva}'
