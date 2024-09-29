from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Cliente, Habitacion, Reserva, Empleado, Usuario
from .forms import ClienteForm, HabitacionForm, ReservaForm, EmpleadoForm


def landing (request):
    return render (request, 'core/landing.html')

def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            usuario = Usuario.objects.get(usuario_nombre=username)
            if usuario.usuario_contrasena == password:
                login(request, usuario)
                
                if usuario.usuario_tipo == 'administrador':
                    return redirect('admin_home')
                elif usuario.usuario_tipo == 'cliente':
                    return redirect('home_cliente')
                elif usuario.usuario_tipo == 'empleado':
                    return redirect('home_cliente')
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Usuario.DoesNotExist:
            messages.error(request, 'El usuario no existe')

    return render(request, 'core/inicio_sesion.html')

def registro(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('inicio_sesion')
    else:
        form = ClienteForm()

    return render(request, 'core/registro.html', {'form': form})

def home_cliente(request):
    return render(request, 'core/home_cliente.html' )


# # # # FUNCIONES ADMINISTRADOR

def admin_home(request):
    return render(request, 'admin_home.html')

#CRUD HABITACIONES

def admin_habitacion_list(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'admin_habitacion_list.html', {'habitaciones': habitaciones})

def admin_habitacion_create(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_habitacion_list')
    else:
        form = HabitacionForm()
    return render(request, 'admin_habitacion_form.html', {'form': form})

def admin_habitacion_update(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        form = HabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            return redirect('admin_habitacion_list')
    else:
        form = HabitacionForm(instance=habitacion)
    return render(request, 'admin_habitacion_form.html', {'form': form})

def admin_habitacion_delete(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        habitacion.delete()
        return redirect('admin_habitacion_list')

#CRUD CLIENTES

def admin_cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'admin_cliente_list.html', {'clientes': clientes})

def admin_cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'admin_cliente_form.html', {'form': form})

def admin_cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('admin_cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'admin_cliente_form.html', {'form': form})

def admin_cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('admin_cliente_list')

#CRUD RESERVAS

def admin_reserva_list(request):
    reservas = Reserva.objects.all()
    return render(request, 'admin_reserva_list.html', {'reservas': reservas})

def admin_reserva_create(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_reserva_list')
    else:
        form = ReservaForm()
    return render(request, 'admin_reserva_form.html', {'form': form})

def admin_reserva_update(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('admin_reserva_list')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'admin_reserva_form.html', {'form': form})

def admin_reserva_delete(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        return redirect('admin_reserva_list')

#CRUD EMPLEADOS

def admin_empleado_list(request):
    empleados = Empleado.objects.all()
    return render(request, 'admin_empleado_list.html', {'empleados': empleados})

def admin_empleado_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_empleado_list')
    else:
        form = EmpleadoForm()
    return render(request, 'admin_empleado_form.html', {'form': form})

def admin_empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('admin_empleado_list')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'admin_empleado_form.html', {'form': form})

def admin_empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('admin_empleado_list')
