from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, Habitacion, Reserva, Empleado, UserProfile

# class RegistroForm(UserCreationForm):
#     nombre = forms.CharField(max_length=100, required=True)
#     apellidos = forms.CharField(max_length=100, required=True)
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2', 'nombre', 'apellidos')

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#             # Crear el cliente asociado
#             Cliente.objects.create(
#                 cliente_nombre=self.cleaned_data['nombre'],
#                 cliente_apellidos=self.cleaned_data['apellidos'],
#                 cliente_email=self.cleaned_data['email'],
#                 usuario=user
#             )
#         return user

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cliente_nombre', 'cliente_apellidos', 'cliente_email', 'cliente_telefono']

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['habitacion_numero', 'habitacion_categoria', 'habitacion_descripcion', 'habitacion_precio', 'hotel']

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['empleado_nombre', 'empleado_apellidos', 'empleado_rol', 'empleado_email', 'empleado_telefono', 'usuario']

