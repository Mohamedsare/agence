from .models import Service
from .forms import ContactForm


def navigation(request):
    """Context processor pour la navigation."""
    return {
        'services': Service.objects.filter(active=True).order_by('order', 'name'),
        'form': ContactForm(),  # Formulaire pour le modal
    }
