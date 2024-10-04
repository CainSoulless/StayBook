from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Cliente, Habitacion, Reserva, Empleado, Administrador
from .forms import ClienteForm, HabitacionForm, EmpleadoForm
import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect
from django.http import HttpRequest

def inicio(request):
    return redirect('landing_page')

def landing_page(request):
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
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'core/inicio_sesion.html')

def registro(request):
    if request.method == 'POST':
        nombre_completo = request.POST['nombre_completo']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']

        # Verificar que las contraseñas coincidan
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('registro')

        # Crear el usuario
        try:
            user = User.objects.create_user(username=email, email=email, password=password1)
            user.save()

            # Crear el cliente asociado
            cliente = Cliente(usuario=user, cliente_nombre=nombre_completo, cliente_email=email)
            cliente.save()

            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect('login')  # Redirigir a la página de login o donde prefieras
        except Exception as e:
            messages.error(request, "Ocurrió un error al registrar el usuario.")
            return redirect('registro')

    return render(request, 'registration/registro.html')

@login_required
def cliente_home(request):
    return render(request, 'core/clientes/cliente_home.html')

@login_required
def cliente_datos(request):
    return render(request, 'core/cliente_datos.html')

@login_required
def home_cliente(request):
    return render(request, 'home_cliente.html')

@login_required
def reserva_habitacion(request, habitacion_id):
    if request.method == 'POST':
        habitacion = get_object_or_404(Habitacion, id=habitacion_id)
        # Verifica si el usuario tiene un perfil de cliente o administrador
        try:
            cliente = request.user.cliente
        except Cliente.DoesNotExist:
            try:
                cliente = request.user.administrador
            except Administrador.DoesNotExist:
                messages.error(request, 'No tienes un perfil de cliente o administrador asociado.')
                return redirect('detalle_habitacion', habitacion_id=habitacion_id)

        metodo_pago = request.POST.get('metodo_pago')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        # Convertir las fechas del formulario en objetos de tipo date
        fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin_obj = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

        # Calcular el número total de días de la reserva
        total_dias = (fecha_fin_obj - fecha_inicio_obj).days

        # Crear la reserva en la base de datos
        nueva_reserva = Reserva.objects.create(
            reserva_fecha=timezone.now().date(),
            reserva_fecha_inicio=fecha_inicio_obj,
            reserva_fecha_fin=fecha_fin_obj,
            reserva_total_dias=total_dias,
            reserva_estado='Confirmada',
            usuario=request.user,  # Cambié aquí a 'usuario'
            habitacion=habitacion,
            tipo_pago=metodo_pago
        )

        # Redirigir al historial de reservas o a otra página que consideres adecuada
        return redirect('historial_reservas')

    return redirect('detalle_habitacion', habitacion_id=habitacion_id)

@login_required
def historial_reservas(request):
    # Obtén todas las reservas del usuario actual
    reservas = Reserva.objects.filter(usuario=request.user)  # Usamos el campo 'usuario' en lugar de 'cliente'

    return render(request, 'core/clientes/historial_reservas.html', {'reservas': reservas})

@login_required
def cliente_datos(request):
    usuario = request.user
    try:
        # Obtener la última reserva del usuario
        ultima_reserva = Reserva.objects.filter(usuario=usuario).order_by('-reserva_fecha').first()
    except Reserva.DoesNotExist:
        ultima_reserva = None

    return render(request, 'core/clientes/cliente_datos.html', {
        'usuario': usuario,
        'ultima_reserva': ultima_reserva
    })

# # # # FUNCIONES ADMINISTRADOR

def adminrf_home(request):
    return render(request, 'core/adminrf_home.html')

#CRUD HABITACIONES

def adminrf_habitacion_list(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'core/adminrf_habitacion_list.html', {'habitaciones': habitaciones})

def adminrf_habitacion_create(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminrf_habitacion_list')
    else:
        form = HabitacionForm()
    return render(request, 'core/adminrf_habitacion_form.html', {'form': form})

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

def adminrf_habitacion_delete(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        habitacion.delete()
        return redirect('adminrf_habitacion_list')

#CRUD CLIENTES

def adminrf_cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'core/adminrf_cliente_list.html', {'clientes': clientes})

def adminrf_cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminrf_cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'core/adminrf_cliente_form.html', {'form': form})

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

def adminrf_cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('adminrf_cliente_list')

#CRUD RESERVAS

def adminrf_reserva_list(request):
    reservas = Reserva.objects.all()
    return render(request, 'core/adminrf_reserva_list.html', {'reservas': reservas})

def adminrf_reserva_create(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminrf_reserva_list')
    else:
        form = ReservaForm()
    return render(request, 'core/adminrf_reserva_form.html', {'form': form})

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

def adminrf_reserva_delete(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        return redirect('adminrf_reserva_list')

#CRUD EMPLEADOS

def adminrf_empleado_list(request):
    empleados = Empleado.objects.all()
    return render(request, 'core/adminrf_empleado_list.html', {'empleados': empleados})

def adminrf_empleado_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminrf_empleado_list')
    else:
        form = EmpleadoForm()
    return render(request, 'core/adminrf_empleado_form.html', {'form': form})

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

def adminrf_empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('adminrf_empleado_list')

def procesar_reserva(request):
    if request.method == 'POST':
        # Aquí procesas el formulario de reserva
        # Si todo está bien, puedes redirigir a otra página
        return redirect('cliente_home')  # O donde quieras redirigir después de la reserva

    return render(request, 'core/reserva_habitacion.html')

def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'core/lista_habitaciones.html', {'habitaciones': habitaciones})

def detalle_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    return render(request, 'core/detalle_habitacion.html', {'habitacion': habitacion})
