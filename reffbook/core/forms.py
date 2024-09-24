from django import forms
from .models import Cliente, Habitacion, Reserva

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cliente_nombre', 'cliente_apellidos', 'cliente_email', 'cliente_telefono']

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['habitacion_numero', 'habitacion_categoria', 'habitacion_descripcion', 'habitacion_precio', 'hotel']

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['reserva_fecha', 'reserva_fecha_inicio', 'reserva_fecha_fin', 'reserva_total_dias', 'reserva_estado', 'cliente', 'habitacion']
