from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Article, Service


class BlogSitemap(Sitemap):
    """Sitemap pour les articles de blog."""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Article.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at


class ServiceSitemap(Sitemap):
    """Sitemap pour les services."""
    changefreq = 'monthly'
    priority = 0.9  # Priorité élevée pour les services

    def items(self):
        return Service.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None
    
    def location(self, obj):
        return obj.get_absolute_url()


class StaticSitemap(Sitemap):
    """Sitemap pour les pages statiques (SEO Burkina Faso : pages locales priorisées)."""
    changefreq = 'monthly'
    priority = 1.0

    # Priorité élevée pour les pages ciblées Burkina Faso / SEO local
    PRIORITIES = {
        'home': 1.0,
        'services_list': 0.95,
        'maintenance_page': 0.92,
        'contact': 0.95,
        'seo_ouagadougou': 0.95,
        'seo_bobo': 0.95,
        'about': 0.9,
        'blog_list': 0.9,
        'team': 0.85,
    }

    def items(self):
        return [
            'home',
            'services_list',
            'maintenance_page',
            'about',
            'team',
            'contact',
            'blog_list',
            'seo_ouagadougou',
            'seo_bobo',
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.PRIORITIES.get(item, 0.8)
