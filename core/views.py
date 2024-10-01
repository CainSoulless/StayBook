from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Cliente, Habitacion, Reserva, Empleado, Usuario
from .forms import ClienteForm, HabitacionForm, ReservaForm, EmpleadoForm, RegistroForm

def landing (request):
    return render (request, 'core/landing.html')

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
            return redirect('inicio_sesion')
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})

def cliente_home(request):
    return render(request, 'core/cliente_home.html')

def historial_reservas(request):
    return render(request, 'core/historial_reservas.html')

def reserva_habitacion(request):
    return render(request, 'core/reserva_habitacion.html')

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
