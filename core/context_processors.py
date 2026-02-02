from .models import Service, WhatsAppConfig
from .forms import ContactForm
from django.db import DatabaseError


def navigation(request):
    """Context processor pour la navigation."""
    try:
        whatsapp_config = WhatsAppConfig.objects.filter(active=True).first()
        services = Service.objects.filter(active=True).order_by('order', 'name')
    except (DatabaseError, Exception):
        # En cas d'erreur de base de données, retourner des valeurs par défaut
        whatsapp_config = None
        services = []
    
    try:
        form = ContactForm()
    except Exception:
        form = None
    
    return {
        'services': services,
        'form': form,
        'whatsapp_config': whatsapp_config,
    }
