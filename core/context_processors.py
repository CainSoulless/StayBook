from .models import Hotel

def hotel_context(request):
    """
    Devuelve el hotel principal (single-tenant) para que esté disponible en todos los templates.
    """
    hotel = Hotel.objects.first()
    return {'hotel': hotel}
