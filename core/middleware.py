"""
Middleware pour tracker les visites sur le site.
Une même page vue par la même session (ou la même IP si pas de session) dans les 24 h
ne compte qu'une seule fois, pour éviter de compter chaque rechargement ou changement de page.
Géolocalisation par IP via ip-api.com (gratuit, cache 24h).
"""
import re
from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache
from .models import PageView


def get_device_type(user_agent):
    """
    Détermine le type d'appareil à partir du User-Agent.
    Ordre : tablette → mobile → desktop → other.
    """
    if not user_agent:
        return PageView.DEVICE_OTHER
    ua = user_agent.lower()
    # Tablettes (avant mobile car iPad contient "mobile")
    if any(x in ua for x in ('ipad', 'tablet', 'playbook', 'silk/', 'kftt', 'kindle', 'gt-p', 'sm-t', 'tab')):
        return PageView.DEVICE_TABLET
    # Mobile
    if any(x in ua for x in ('mobile', 'android', 'iphone', 'ipod', 'webos', 'blackberry', 'opera mini', 'iemobile', 'windows phone')):
        return PageView.DEVICE_MOBILE
    # Desktop (navigateurs classiques)
    if any(x in ua for x in ('windows', 'macintosh', 'linux', 'x11', 'cros', 'openbsd')):
        return PageView.DEVICE_DESKTOP
    return PageView.DEVICE_OTHER


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
        """
        Obtenir pays, code pays et ville depuis l'IP via ip-api.com.
        Résultat mis en cache 24h par IP pour respecter la limite (45 req/min).
        """
        if not ip_address or ip_address in ('127.0.0.1', '::1'):
            return None, None, None
        # IPs privées : pas d'appel API
        if ip_address.startswith(('10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21.', '172.22.', '172.23.', '172.24.', '172.25.', '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.', '192.168.')):
            return None, None, None
        cache_key = f"geo_ip_{ip_address}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        try:
            import urllib.request
            url = f"http://ip-api.com/json/{ip_address}?fields=status,country,countryCode,city"
            req = urllib.request.Request(url, headers={'User-Agent': 'FasowebStats/1.0'})
            with urllib.request.urlopen(req, timeout=2) as resp:
                data = resp.read().decode()
            import json
            info = json.loads(data)
            if info.get('status') == 'success':
                result = (info.get('country') or '', (info.get('countryCode') or '')[:2], info.get('city') or '')
                cache.set(cache_key, result, 86400)  # 24h
                return result
        except Exception:
            pass
        cache.set(cache_key, (None, None, None), 300)  # 5 min en cas d'échec pour ne pas surcharger
        return None, None, None
    
    def track_page_view(self, request):
        """
        Enregistre une visite de page.
        Une même page par même visiteur (session ou IP) ne compte qu'une fois sur 24 h.
        """
        if not self.should_track(request):
            return
        
        try:
            ip_address = request.META.get('REMOTE_ADDR', '')
            if not ip_address:
                return
            
            path = request.path[:500]
            cutoff = timezone.now() - timedelta(hours=24)
            
            # Utiliser la session si disponible pour dédupliquer (une visite par page par session sur 24 h)
            session_key = ''
            if hasattr(request, 'session') and request.session.session_key:
                session_key = request.session.session_key
            
            if session_key:
                already = PageView.objects.filter(
                    path=path,
                    session_key=session_key,
                    created_at__gte=cutoff,
                ).exists()
            else:
                already = PageView.objects.filter(
                    path=path,
                    ip_address=ip_address,
                    created_at__gte=cutoff,
                ).exists()
            
            if already:
                return
            
            country, country_code, city = self.get_country_from_ip(ip_address)
            referer = (request.META.get('HTTP_REFERER') or '')[:2000]
            user_agent = (request.META.get('HTTP_USER_AGENT') or '')[:500]
            device_type = get_device_type(user_agent)
            
            PageView.objects.create(
                path=path,
                ip_address=ip_address,
                session_key=session_key,
                device_type=device_type,
                country=country or '',
                country_code=country_code or '',
                city=city or '',
                user_agent=user_agent,
                referer=referer,
                is_bot=self.is_bot(request.META.get('HTTP_USER_AGENT', '')),
            )
        except Exception:
            pass
