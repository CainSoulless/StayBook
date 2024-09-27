from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Habitacion, Reserva
from .forms import ClienteForm, HabitacionForm, ReservaForm


def landing (request):
    return render (request, 'core/landing.html')

def inicio_sesion(request):
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

# Vista para listar habitaciones
def habitacion_list(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'core/habitacion_list.html', {'habitaciones': habitaciones})

# Vista para crear una nueva habitación
def habitacion_create(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('habitacion_list')
    else:
        form = HabitacionForm()
    return render(request, 'core/habitacion_form.html', {'form': form})

# Vista para actualizar una habitación existente
def habitacion_update(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        form = HabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            return redirect('habitacion_list')
    else:
        form = HabitacionForm(instance=habitacion)
    return render(request, 'core/habitacion_form.html', {'form': form})

# Vista para eliminar una habitación
def habitacion_delete(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        habitacion.delete()
        return redirect('habitacion_list')
    return render(request, 'core/habitacion_confirm_delete.html', {'habitacion': habitacion})