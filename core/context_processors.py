from .models import Service, WhatsAppConfig
from .forms import ContactForm


def navigation(request):
    """Context processor pour la navigation."""
    whatsapp_config = WhatsAppConfig.objects.filter(active=True).first()
    return {
        'services': Service.objects.filter(active=True).order_by('order', 'name'),
        'form': ContactForm(),  # Formulaire pour le modal
        'whatsapp_config': whatsapp_config,
    }
