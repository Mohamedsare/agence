from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from .models import Article, Service


class BlogSitemap(Sitemap):
    """Sitemap pour les articles de blog. Priority 0.6 (recommandation SEO)."""
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Article.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at


class ServiceSitemap(Sitemap):
    """Sitemap pour les pages services (détail). Priority 0.8. Inclut maintenance-site-web."""
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Service.objects.filter(active=True)

    def lastmod(self, obj):
        # Service n'a pas updated_at, on utilise la date du jour pour lastmod
        return getattr(obj, 'updated_at', None) or timezone.now()

    def location(self, obj):
        return obj.get_absolute_url()


class StaticSitemap(Sitemap):
    """
    Sitemap pour les pages statiques.
    - Pas de maintenance_page ici : l'URL /services/maintenance-site-web/ est déjà
      fournie par ServiceSitemap (service slug=maintenance-site-web), évitant le doublon.
    - lastmod sur toutes les URLs pour le SEO.
    - Priorités : Home 1.0, Services 0.9, pages secondaires 0.7-0.8.
    """
    changefreq = 'monthly'
    priority = 0.8

    PRIORITIES = {
        'home': 1.0,
        'services_list': 0.9,
        'contact': 0.7,
        'about': 0.8,
        'team': 0.7,
        'blog_list': 0.7,
        'seo_ouagadougou': 0.8,
        'seo_bobo': 0.8,
        'legal': 0.5,
        'privacy': 0.5,
    }

    CHANGEFREQ = {
        'home': 'weekly',
        'services_list': 'monthly',
        'contact': 'yearly',
        'about': 'monthly',
        'team': 'monthly',
        'blog_list': 'weekly',
        'seo_ouagadougou': 'monthly',
        'seo_bobo': 'monthly',
        'legal': 'yearly',
        'privacy': 'yearly',
    }

    def items(self):
        return [
            'home',
            'services_list',
            'about',
            'team',
            'contact',
            'blog_list',
            'seo_ouagadougou',
            'seo_bobo',
            'legal',
            'privacy',
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.PRIORITIES.get(item, 0.8)

    def changefreq(self, item):
        return self.CHANGEFREQ.get(item, 'monthly')

    def lastmod(self, item):
        return timezone.now()


# Pages SEO recommandées à ajouter quand les vues/URLs existeront :
# - /creation-site-web-burkina-faso/  (priority 0.8)
# - /agence-web-burkina-faso/         (priority 0.8)
# - /developpeur-web-ouagadougou/      (priority 0.8)
# - /prix-site-web-burkina-faso/      (priority 0.8)
