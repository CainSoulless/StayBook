from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Habitacion, Reserva


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
        fields = ["numero", "categoria", "descripcion", "precio", "hotel", "imagen"]


# ======================
# CRUD RESERVAS
# ======================
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["fecha_inicio", "fecha_fin", "estado", "tipo_pago", "cliente", "habitacion"]


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
