"""
WSGI config for FASOWEB project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siraweb.settings')

application = get_wsgi_application()
