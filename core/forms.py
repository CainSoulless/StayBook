from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Habitacion, Reserva, Hotel


# ======================
# AUTENTICACIÓN
# ======================
class RegistroForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.USER_TYPES)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "telefono", "role", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuario o Email")
    password = forms.CharField(widget=forms.PasswordInput)


# ======================
# CRUD HABITACIONES
# ======================
class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['numero', 'categoria', 'descripcion', 'precio', 'hotel', 'imagen']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'hotel': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# ======================
# CRUD RESERVAS
# ======================
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'habitacion', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'habitacion': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Selecciona una fecha de inicio'
                }
            ),
            'fecha_fin': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Selecciona una fecha de fin'
                }
            ),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }


# ======================
# USUARIOS (Cliente / Empleado)
# ======================
class ClienteForm(forms.ModelForm):
    """Formulario para editar clientes (usuarios con role=cliente)."""

    class Meta:
        model = CustomUser
        fields = ["username", "email", "telefono"]


class EmpleadoForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'empleado'  # Forzar rol automáticamente
        if commit:
            user.save()
        return user


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["nombre", "direccion", "correo_contacto", "logo"]

# class HotelForm(forms.ModelForm):
#     class Meta:
#         model = Hotel
#         fields = ['nombre', 'direccion', 'logo', 'correo_contacto']
#         widgets = {
#             'nombre': forms.TextInput(attrs={'class': 'form-control'}),
#             'direccion': forms.TextInput(attrs={'class': 'form-control'}),
#             'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#             'correo_contacto': forms.EmailInput(attrs={'class': 'form-control'}),
#         }
