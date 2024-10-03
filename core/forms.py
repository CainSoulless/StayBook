from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, Habitacion, Reserva, Empleado, UserProfile

class RegistroForm(UserCreationForm):
    USER_TYPES = (
        ('cliente', 'Cliente'),
        ('empleado', 'Empleado'),
        ('administrador', 'Administrador'),
    )

    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=USER_TYPES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_profile = UserProfile.objects.create(
                user=user, 
                user_type=self.cleaned_data['user_type']
            )
            user_profile.save()
        return user

# class RegistroForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True, label='Nombre')
#     last_name = forms.CharField(max_length=30, required=True, label='Apellido')
#     email = forms.EmailField(required=True, label='Email')

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
    
#     def __init__(self, *args, **kwargs):
#         super(RegistroForm, self).__init__(*args, **kwargs)
#         for fieldname in ['username', 'password1', 'password2']:
#             self.fields[fieldname].help_text = None

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cliente_nombre', 'cliente_apellidos', 'cliente_email', 'cliente_telefono']

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['habitacion_numero', 'habitacion_categoria', 'habitacion_descripcion', 'habitacion_precio', 'hotel']

# class ReservaForm(forms.ModelForm):
#     class Meta:
#         model = Reserva
#         fields = ['reserva_fecha', 'reserva_fecha_inicio', 'reserva_fecha_fin', 'reserva_total_dias', 'reserva_estado', 'cliente', 'habitacion']

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['empleado_nombre', 'empleado_apellidos', 'empleado_rol', 'empleado_email', 'empleado_telefono', 'usuario']

