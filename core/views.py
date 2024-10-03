from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente, Habitacion, Reserva, Empleado, Administrador
from .forms import ClienteForm, HabitacionForm, EmpleadoForm, RegistroForm
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
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a la página de login después del registro
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})


def cliente_home(request):
    return render(request, 'core/clientes/cliente_home.html')

def cliente_datos(request):
    return render(request, 'core/cliente_datos.html')

def home_cliente(request):
    return render(request, 'home_cliente.html')


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
            cliente=cliente,
            habitacion=habitacion,
            tipo_pago=metodo_pago
        )

        # Redirigir al historial de reservas o a otra página que consideres adecuada
        return redirect('historial_reservas')

    return redirect('detalle_habitacion', habitacion_id=habitacion_id)

@login_required
def historial_reservas(request):
    # Obtén el cliente asociado al usuario actual
    try:
        cliente = request.user.cliente  # Esto asume que ya has configurado la relación correctamente
        reservas = Reserva.objects.filter(cliente=cliente)
    except Cliente.DoesNotExist:
        reservas = []  # Si no existe, puedes manejarlo de la forma que desees

    return render(request, 'core/clientes/historial_reservas.html', {'reservas': reservas})