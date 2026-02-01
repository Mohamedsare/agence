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
    priority = 0.8

    def items(self):
        return Service.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None


class StaticSitemap(Sitemap):
    """Sitemap pour les pages statiques."""
    changefreq = 'monthly'
    priority = 1.0

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
        ]

    def location(self, item):
        return reverse(item)
