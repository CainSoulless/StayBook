from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

from .models import Habitacion, Reserva, Hotel, CustomUser
from .forms import HabitacionForm, ReservaForm, RegistroForm, EmpleadoForm, HotelForm

# Token invitation
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from core.utils.tokens import account_activation_token

# Activación de cuenta
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login

User = get_user_model()


def landing_page(request):
    """Landing page."""
    return render(request, 'core/landing_page.html')


def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('cliente_home')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return redirect('login')
    # return render(request, 'core/login.html')
    return redirect("registration/login.html")


def registro(request):
    """Registro de un nuevo usuario (cliente)."""
    if request.method == 'POST':
        nombre_completo = request.POST['nombre_completo']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('registro')

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password1,
                role="cliente"
            )
            user.first_name = nombre_completo
            user.save()
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect('login')
        except Exception:
            messages.error(request, "Ocurrió un error al registrar el usuario.")
            return redirect('registro')

    return render(request, 'registration/registro.html')


#@login_required
def cliente_home(request):
    hotel = Hotel.objects.first()
    if not hotel:
        return render(request, 'core/error_no_hotel.html')
    habitaciones = Habitacion.objects.filter(hotel=hotel)
    return render(request, 'core/clientes/cliente_home.html', {
        'hotel': hotel,
        'habitaciones': habitaciones,
    })


@login_required
def cliente_datos(request):
    """Muestra los datos del cliente y su última reserva."""
    user = request.user
    ultima_reserva = None
    es_admin = user.is_superuser or user.role == "administrador"

    if user.role == "cliente":
        ultima_reserva = Reserva.objects.filter(cliente=user).order_by('-fecha_creacion').first()

    return render(request, 'core/clientes/cliente_datos.html', {
        'cliente': user if user.role == "cliente" else None,
        'ultima_reserva': ultima_reserva,
        'es_admin': es_admin,
    })


@login_required
def reserva_habitacion(request, habitacion_id):
    """Manejo de reservas de habitaciones."""
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)

    if request.method == 'POST':
        if request.user.role != "cliente":
            messages.error(request, 'Solo los clientes pueden reservar.')
            return redirect('detalle_habitacion', habitacion_id=habitacion_id)

        metodo_pago = request.POST.get('metodo_pago')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin_obj = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        total_dias = (fecha_fin_obj - fecha_inicio_obj).days

        Reserva.objects.create(
            fecha_inicio=fecha_inicio_obj,
            fecha_fin=fecha_fin_obj,
            total_dias=total_dias,
            estado='Confirmada',
            cliente=request.user,
            habitacion=habitacion,
            tipo_pago=metodo_pago
        )

        return redirect('historial_reservas')

    return redirect('detalle_habitacion', habitacion_id=habitacion_id)


@login_required
def historial_reservas(request):
    """Muestra el historial de reservas del usuario."""
    reservas = Reserva.objects.filter(cliente=request.user)
    return render(request, 'core/clientes/historial_reservas.html', {'reservas': reservas})


# ---------------------- ADMIN VIEWS ----------------------

@login_required
def adminrf_home(request):
    """Dashboard de administrador."""
    return render(request, 'core/admin_panel/adminrf_home.html')


# CRUD HABITACIONES
@login_required
def adminrf_habitacion_list(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'core/admin_panel/adminrf_habitacion_list.html', {'habitaciones': habitaciones})


@login_required
def adminrf_habitacion_create(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminrf_habitacion_list')
    else:
        form = HabitacionForm()
    return render(request, 'core/admin_panel/adminrf_habitacion_form.html', {'form': form})


@login_required
def adminrf_habitacion_update(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        form = HabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            return redirect('adminrf_habitacion_list')
    else:
        form = HabitacionForm(instance=habitacion)
    return render(request, 'core/admin_panel/adminrf_habitacion_form.html', {'form': form})


@login_required
def adminrf_habitacion_delete(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        habitacion.delete()
        return redirect('core/admin_panel/adminrf_habitacion_list')


# ---------------------- GENERAL VIEWS ----------------------

def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'core/lista_habitaciones.html', {'habitaciones': habitaciones})


def detalle_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    return render(request, 'core/detalle_habitacion.html', {'habitacion': habitacion})


# ---------------------- INVITACIONES ----------------------

def invite_admin(request, hotel_id):
    """Crea un usuario administrador inactivo y envía invitación por email."""
    hotel = Hotel.objects.get(id=hotel_id)
    user = User.objects.create_user(
        username=hotel.nombre.lower(),
        email=hotel.correo_contacto,
        password=None,
        role="administrador",
        is_active=False
    )

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    domain = get_current_site(request).domain
    activation_link = f"http://{domain}/activate/{uid}/{token}/"

    subject = "Invitación para administrar tu hotel en StayBook"
    message = render_to_string("emails/invite_admin.html", {
        'hotel': hotel,
        'activation_link': activation_link,
    })
    send_mail(subject, message, "no-reply@staybook.com", [user.email])


def activar_cuenta(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                user.set_password(password1)
                user.is_active = True
                user.save()
                login(request, user)
                messages.success(request, "Tu cuenta ha sido activada con éxito.")
                return redirect('adminrf_home')
            else:
                messages.error(request, "Las contraseñas no coinciden.")
        return render(request, 'registration/activar_cuenta.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, "El enlace de activación no es válido o ha expirado.")
        return redirect('login')

# ======================
# PANEL ADMIN HOME
# ======================
@login_required
def adminrf_home(request):
    return render(request, "core/admin_panel/adminrf_home.html")


# ======================
# CRUD HABITACIONES
# ======================
@login_required
def adminrf_habitacion_list(request):
    habitaciones = Habitacion.objects.all()
    return render(request, "core/admin_panel/adminrf_habitacion_list.html", {"habitaciones": habitaciones})


@login_required
def adminrf_habitacion_create(request):
    if request.method == "POST":
        form = HabitacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Habitación creada correctamente.")
            return redirect("admin_panel:habitacion_list")
    else:
        form = HabitacionForm()
    return render(request, "core/admin_panel/adminrf_habitacion_form.html", {"form": form})


@login_required
def adminrf_habitacion_update(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == "POST":
        form = HabitacionForm(request.POST, request.FILES, instance=habitacion)
        if form.is_valid():
            form.save()
            messages.success(request, "Habitación actualizada correctamente.")
            return redirect("admin_panel:habitacion_list")
    else:
        form = HabitacionForm(instance=habitacion)
    return render(request, "core/admin_panel/adminrf_habitacion_form.html", {"form": form})


@login_required
def adminrf_habitacion_delete(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == "POST":
        habitacion.delete()
        messages.success(request, "Habitación eliminada correctamente.")
        return redirect("admin_panel:habitacion_list")
    return render(request, "core/admin_panel/adminrf_habitacion_confirm_delete.html", {"habitacion": habitacion})


# ======================
# CRUD CLIENTES (CustomUser con rol cliente)
# ======================

@login_required
def adminrf_cliente_create(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.role = "cliente"  # asignamos rol cliente
            cliente.save()
            return redirect("adminrf_cliente_list")
    else:
        form = RegistroForm()
    return render(request, "core/admin_panel/adminrf_cliente_form.html", {"form": form})

@login_required
def adminrf_cliente_list(request):
    clientes = CustomUser.objects.filter(role="cliente")
    return render(request, "core/admin_panel/adminrf_cliente_list.html", {"clientes": clientes})


@login_required
def adminrf_cliente_delete(request, pk):
    cliente = get_object_or_404(CustomUser, pk=pk, role="cliente")
    if request.method == "POST":
        cliente.delete()
        messages.success(request, "Cliente eliminado correctamente.")
        return redirect("admin_panel:cliente_list")
    return render(request, "core/admin_panel/adminrf_cliente_confirm_delete.html", {"cliente": cliente})

@login_required
def adminrf_cliente_update(request, pk):
    cliente = get_object_or_404(CustomUser, pk=pk, role="cliente")
    if request.method == "POST":
        form = RegistroForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("adminrf_cliente_list")
    else:
        form = RegistroForm(instance=cliente)
    return render(request, "core/admin_panel/adminrf_cliente_form.html", {"form": form})



# ======================
# CRUD RESERVAS
# ======================
@login_required
def adminrf_reserva_list(request):
    reservas = Reserva.objects.select_related("cliente", "habitacion")
    return render(request, "core/admin_panel/adminrf_reserva_list.html", {"reservas": reservas})


@login_required
def adminrf_reserva_create(request):
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Reserva creada correctamente.")
            return redirect("admin_panel:reserva_list")
    else:
        form = ReservaForm()
    return render(request, "core/admin_panel/adminrf_reserva_form.html", {"form": form})


@login_required
def adminrf_reserva_update(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == "POST":
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "Reserva actualizada correctamente.")
            return redirect("admin_panel:reserva_list")
    else:
        form = ReservaForm(instance=reserva)
    return render(request, "core/admin_panel/adminrf_reserva_form.html", {"form": form})


@login_required
def adminrf_reserva_delete(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == "POST":
        reserva.delete()
        messages.success(request, "Reserva eliminada correctamente.")
        return redirect("admin_panel:reserva_list")
    return render(request, "core/admin_panel/adminrf_reserva_confirm_delete.html", {"reserva": reserva})


# ======================
# CRUD EMPLEADOS (CustomUser con rol empleado)
# ======================
@login_required
def adminrf_empleado_list(request):
    empleados = CustomUser.objects.filter(role="empleado")
    return render(request, "core/admin_panel/adminrf_empleado_list.html", {"empleados": empleados})

# CREAR EMPLEADO
@login_required
def adminrf_empleado_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminrf_empleado_list')
    else:
        form = EmpleadoForm()
    return render(request, 'core/admin_panel/adminrf_empleado_form.html', {'form': form})


# ACTUALIZAR EMPLEADO
@login_required
def adminrf_empleado_update(request, pk):
    empleado = get_object_or_404(CustomUser, pk=pk, role="empleado")
    if request.method == "POST":
        form = RegistroForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect("adminrf_empleado_list")
    else:
        form = RegistroForm(instance=empleado)
    return render(request, "core/admin_panel/adminrf_empleado_form.html", {"form": form})

# ELIMINAR EMPLEADO
@login_required
def adminrf_empleado_delete(request, pk):
    empleado = get_object_or_404(CustomUser, pk=pk, role="empleado")
    if request.method == "POST":
        empleado.delete()
        return redirect("adminrf_empleado_list")
    return render(request, "core/admin_panel/adminrf_empleado_confirm_delete.html", {"empleado": empleado})

@login_required
def adminrf_hotel_update(request):
    """Permite al administrador crear o editar su hotel directamente."""
    user = request.user
    print(f"[DEBUG] Usuario: {user.username}, Rol: '{user.role}'")

    # Solo administradores pueden acceder
    if user.role.strip().lower() != "administrador":
        return redirect("adminrf_home")

    # Buscar el hotel asociado o crear uno nuevo asignado al usuario
    hotel = Hotel.objects.filter(administrador=user).first()

    if not hotel:
        # Si el usuario no tiene hotel asignado, intenta recuperar alguno sin administrador
        hotel = Hotel.objects.filter(administrador__isnull=True).first()
        if hotel:
            hotel.administrador = user
            hotel.save()
            print("[DEBUG] Se asignó hotel existente al administrador.")
        else:
            hotel = Hotel.objects.create(administrador=user, nombre="Nuevo Hotel")
            print("[DEBUG] No había hotel, se creó uno nuevo.")

    # Procesar formulario
    if request.method == "POST":
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.instance.administrador = user
            form.save()
            print("[DEBUG] Hotel actualizado correctamente.")
            return redirect("adminrf_home")
        else:
            print("[DEBUG] Errores en el formulario:", form.errors)
    else:
        form = HotelForm(instance=hotel)

    return render(request, "core/admin_panel/adminrf_hotel_form.html", {"form": form})
