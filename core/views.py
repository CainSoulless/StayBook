from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Cliente, Habitacion, Reserva, Empleado, Administrador
from .forms import ClienteForm, HabitacionForm, EmpleadoForm
from datetime import datetime
from django.utils import timezone

def landing_page(request):
    """Redirige a cliente_home si el usuario está autenticado."""
    if request.user.is_authenticated:
        return redirect('cliente_home')
    return render(request, 'core/landing_page.html')

def inicio_sesion(request):
    """Manejo del inicio de sesión."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('cliente_home')
        messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'core/inicio_sesion.html')

def registro(request):
    """Registro de un nuevo usuario y cliente."""
    if request.method == 'POST':
        nombre_completo = request.POST['nombre_completo']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('registro')

        try:
            user = User.objects.create_user(username=email, email=email, password=password1)
            Cliente.objects.create(usuario=user, cliente_nombre=nombre_completo, cliente_email=email)
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect('login')
        except Exception:
            messages.error(request, "Ocurrió un error al registrar el usuario.")
            return redirect('registro')

    return render(request, 'registration/registro.html')

@login_required
def cliente_home(request):
    """Página principal para clientes."""
    return render(request, 'core/clientes/cliente_home.html')

@login_required
def cliente_datos(request):
    """Muestra los datos del cliente y su última reserva."""
    user = request.user
    cliente = None
    ultima_reserva = None
    es_admin = user.is_superuser

    if not es_admin:
        try:
            cliente = user.cliente
            ultima_reserva = Reserva.objects.filter(usuario=user).order_by('-reserva_fecha').first()
        except Cliente.DoesNotExist:
            messages.error(request, "No se encontró información del cliente.")

    return render(request, 'core/clientes/cliente_datos.html', {
        'cliente': cliente,
        'ultima_reserva': ultima_reserva,
        'es_admin': es_admin,
    })

@login_required
def reserva_habitacion(request, habitacion_id):
    """Manejo de reservas de habitaciones."""
    habitacion = get_object_or_404(Habitacion, id=habitacion_id)

    if request.method == 'POST':
        try:
            cliente = request.user.cliente
        except Cliente.DoesNotExist:
            messages.error(request, 'No tienes un perfil de cliente asociado.')
            return redirect('detalle_habitacion', habitacion_id=habitacion_id)

        metodo_pago = request.POST.get('metodo_pago')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin_obj = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        total_dias = (fecha_fin_obj - fecha_inicio_obj).days

        Reserva.objects.create(
            reserva_fecha=timezone.now().date(),
            reserva_fecha_inicio=fecha_inicio_obj,
            reserva_fecha_fin=fecha_fin_obj,
            reserva_total_dias=total_dias,
            reserva_estado='Confirmada',
            usuario=request.user,
            habitacion=habitacion,
            tipo_pago=metodo_pago
        )

        return redirect('historial_reservas')

    return redirect('detalle_habitacion', habitacion_id=habitacion_id)

@login_required
def historial_reservas(request):
    """Muestra el historial de reservas del usuario."""
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'core/clientes/historial_reservas.html', {'reservas': reservas})

# CRUD HABITACIONES
@login_required
def adminrf_habitacion_list(request):
    """Lista todas las habitaciones."""
    habitaciones = Habitacion.objects.all()
    return render(request, 'core/adminrf_habitacion_list.html', {'habitaciones': habitaciones})


# # # # FUNCIONES ADMINISTRADOR

@login_required
def adminrf_home(request):
    return render(request, 'core/adminrf_home.html')

#CRUD HABITACIONES

# def adminrf_habitacion_list(request):
#     habitaciones = Habitacion.objects.all()
#     return render(request, 'core/adminrf_habitacion_list.html', {'habitaciones': habitaciones})

@login_required
def adminrf_habitacion_create(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminrf_habitacion_list')
    else:
        form = HabitacionForm()
    return render(request, 'core/adminrf_habitacion_form.html', {'form': form})

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
    return render(request, 'core/adminrf_habitacion_form.html', {'form': form})

@login_required
def adminrf_habitacion_delete(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        habitacion.delete()
        return redirect('adminrf_habitacion_list')

#CRUD CLIENTES

@login_required
def adminrf_cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'core/adminrf_cliente_list.html', {'clientes': clientes})

@login_required
def adminrf_cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminrf_cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'core/adminrf_cliente_form.html', {'form': form})

@login_required
def adminrf_cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('adminrf_cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'core/adminrf_cliente_form.html', {'form': form})

@login_required
def adminrf_cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('adminrf_cliente_list')

#CRUD RESERVAS

@login_required
def adminrf_reserva_list(request):
    reservas = Reserva.objects.all()
    return render(request, 'core/adminrf_reserva_list.html', {'reservas': reservas})

@login_required
def adminrf_reserva_create(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminrf_reserva_list')
    else:
        form = ReservaForm()
    return render(request, 'core/adminrf_reserva_form.html', {'form': form})

@login_required
def adminrf_reserva_update(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('adminrf_reserva_list')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'core/adminrf_reserva_form.html', {'form': form})

@login_required
def adminrf_reserva_delete(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        return redirect('adminrf_reserva_list')

#CRUD EMPLEADOS

@login_required
def adminrf_empleado_list(request):
    empleados = Empleado.objects.all()
    return render(request, 'core/adminrf_empleado_list.html', {'empleados': empleados})

@login_required
def adminrf_empleado_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminrf_empleado_list')
    else:
        form = EmpleadoForm()
    return render(request, 'core/adminrf_empleado_form.html', {'form': form})

@login_required
def adminrf_empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('adminrf_empleado_list')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'core/adminrf_empleado_form.html', {'form': form})

@login_required
def adminrf_empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('adminrf_empleado_list')

@login_required
def procesar_reserva(request):
    if request.method == 'POST':
        # Aquí procesas el formulario de reserva
        # Si todo está bien, puedes redirigir a otra página
        return redirect('cliente_home')  # O donde quieras redirigir después de la reserva

    return render(request, 'core/reserva_habitacion.html')

@login_required
def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'core/lista_habitaciones.html', {'habitaciones': habitaciones})

@login_required
def detalle_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    return render(request, 'core/detalle_habitacion.html', {'habitacion': habitacion})
