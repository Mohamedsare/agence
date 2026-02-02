"""
Middleware pour tracker les visites sur le site.
"""
import re
from django.utils import timezone
from django.core.cache import cache
from .models import PageView


class PageViewTrackingMiddleware:
    """Middleware pour tracker les visites."""
    
    # Patterns pour détecter les bots
    BOT_PATTERNS = [
        r'bot', r'crawler', r'spider', r'scraper',
        r'facebookexternalhit', r'twitterbot', r'linkedinbot',
        r'whatsapp', r'telegram', r'skype', r'googlebot',
        r'bingbot', r'yandex', r'baiduspider', r'duckduckbot'
    ]
    
    # Chemins à ignorer
    IGNORE_PATHS = [
        '/admin/',
        '/static/',
        '/media/',
        '/favicon.ico',
        '/robots.txt',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Tracker la visite avant la réponse
        self.track_page_view(request)
        
        response = self.get_response(request)
        return response
    
    def is_bot(self, user_agent):
        """Vérifier si le user agent est un bot."""
        if not user_agent:
            return False
        user_agent_lower = user_agent.lower()
        return any(re.search(pattern, user_agent_lower) for pattern in self.BOT_PATTERNS)
    
    def should_track(self, request):
        """Déterminer si on doit tracker cette visite."""
        # Ignorer les chemins spécifiques
        if any(request.path.startswith(path) for path in self.IGNORE_PATHS):
            return False
        
        # Ignorer les bots
        if self.is_bot(request.META.get('HTTP_USER_AGENT', '')):
            return False
        
        # Ignorer les requêtes AJAX (optionnel)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return False
        
        return True
    
    def get_country_from_ip(self, ip_address):
        """Obtenir le pays depuis l'IP (simplifié, utiliser un service comme ipapi.co en production)."""
        # Pour l'instant, on retourne None
        # En production, utiliser un service comme ipapi.co, ip-api.com, ou geoip2
        return None, None, None
    
    def track_page_view(self, request):
        """Tracker une visite de page."""
        if not self.should_track(request):
            return
        
        # Créer une clé de cache pour éviter les doublons rapides
        cache_key = f"pageview_{request.path}_{request.META.get('REMOTE_ADDR')}"
        if cache.get(cache_key):
            return
        
        # Mettre en cache pendant 1 minute pour éviter les doublons
        cache.set(cache_key, True, 60)
        
        try:
            ip_address = request.META.get('REMOTE_ADDR', '')
            if not ip_address:
                return
            
            # Obtenir les informations de géolocalisation (simplifié)
            country, country_code, city = self.get_country_from_ip(ip_address)
            
            PageView.objects.create(
                path=request.path[:500],  # Limiter la longueur
                ip_address=ip_address,
                country=country or '',
                country_code=country_code or '',
                city=city or '',
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                referer=request.META.get('HTTP_REFERER', '')[:500],
                is_bot=self.is_bot(request.META.get('HTTP_USER_AGENT', '')),
            )
        except Exception:
            # Ignorer les erreurs pour ne pas casser le site
            pass
