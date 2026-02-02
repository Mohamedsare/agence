from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import Article, Category, Tag, Service, TeamMember, Testimonial, Partner, Portfolio, Technology, AnonymousCTA, FAQ, CompanyStats, PageView
from .forms import ContactForm


def home(request):
    """Page d'accueil."""
    testimonials = Testimonial.objects.filter(active=True).order_by('order')[:6]
    partners = Partner.objects.filter(active=True).order_by('order')[:8]
    portfolio_projects = Portfolio.objects.filter(active=True).order_by('order')[:4]
    technologies = Technology.objects.filter(active=True).order_by('order', 'name')
    services = Service.objects.filter(active=True).order_by('order', 'name')[:6]
    anonymous_cta = AnonymousCTA.objects.filter(active=True).first()
    
    # Pagination des FAQs (8 par page)
    faqs_list = FAQ.objects.filter(active=True).order_by('order', 'question')
    paginator = Paginator(faqs_list, 8)
    page_number = request.GET.get('page')
    faqs = paginator.get_page(page_number)
    
    context = {
        'testimonials': testimonials,
        'partners': partners,
        'portfolio_projects': portfolio_projects,
        'technologies': technologies,
        'services': services,
        'anonymous_cta': anonymous_cta,
        'faqs': faqs,
        'meta_title': 'SiraWeb - Agence Web au Burkina Faso | Création de Sites Web Modernes',
        'meta_description': 'Agence web au Burkina Faso spécialisée dans la création de sites web sur mesure, SEO et développement web moderne. Services à Ouagadougou et Bobo-Dioulasso.',
    }
    return render(request, 'core/home.html', context)


def services_list(request):
    """Liste des services."""
    services = Service.objects.filter(active=True).order_by('order', 'name')
    
    context = {
        'services': services,
        'meta_title': 'Nos Services - Agence Web Burkina Faso | SiraWeb',
        'meta_description': 'Découvrez nos services web : création de sites vitrine, e-commerce, SEO, refonte UI/UX, maintenance et hébergement au Burkina Faso.',
    }
    return render(request, 'core/services_list.html', context)


def service_detail(request, slug):
    """Détail d'un service."""
    service = get_object_or_404(Service, slug=slug, active=True)
    
    # Services similaires
    similar_services = Service.objects.filter(active=True).exclude(id=service.id).order_by('order')[:3]
    
    context = {
        'service': service,
        'similar_services': similar_services,
        'meta_title': service.meta_title or f'{service.get_name_display()} - SiraWeb',
        'meta_description': service.meta_description or service.short_description,
    }
    return render(request, 'core/service_detail.html', context)


def about(request):
    """Page À propos."""
    team_members = TeamMember.objects.filter(active=True).order_by('order', 'name')
    company_stats = CompanyStats.objects.filter(active=True).first()
    
    context = {
        'team_members': team_members,
        'company_stats': company_stats,
        'meta_title': 'À Propos - SiraWeb | Agence Web Burkina Faso',
        'meta_description': 'Découvrez SiraWeb, votre agence web au Burkina Faso. Notre équipe experte vous accompagne dans vos projets web à Ouagadougou et Bobo-Dioulasso.',
    }
    return render(request, 'core/about.html', context)


def team(request):
    """Page Équipe."""
    team_members = TeamMember.objects.filter(active=True).order_by('order', 'name')
    
    context = {
        'team_members': team_members,
        'meta_title': 'Notre Équipe - SiraWeb | Agence Web Burkina Faso',
        'meta_description': 'Rencontrez l\'équipe SiraWeb, des experts en développement web, SEO et design UI/UX au Burkina Faso.',
    }
    return render(request, 'core/team.html', context)


def contact(request):
    """Page de contact."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()
            
            # Envoyer l'email
            subject = f'Nouveau message de contact de {message.name}'
            email_message = f"""
Nom: {message.name}
Email: {message.email}
Téléphone: {message.phone or 'Non renseigné'}
Entreprise: {message.company or 'Non renseigné'}
Budget: {message.budget or 'Non renseigné'}

Message:
{message.message}
"""
            try:
                send_mail(
                    subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
            except Exception:
                pass  # En développement, console backend
            
            messages.success(request, 'Votre message a été envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'meta_title': 'Contact - SiraWeb | Agence Web Burkina Faso',
        'meta_description': 'Contactez SiraWeb pour vos projets web au Burkina Faso. Devis gratuit pour création de site web, SEO, refonte à Ouagadougou et Bobo-Dioulasso.',
    }
    return render(request, 'core/contact.html', context)


def blog_list(request):
    """Liste des articles de blog."""
    articles_list = Article.objects.filter(published=True).order_by('-published_at', '-created_at')
    
    # Pagination
    paginator = Paginator(articles_list, 9)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    
    # Catégories et tags populaires
    categories = Category.objects.all()[:10]
    tags = Tag.objects.all()[:20]
    
    context = {
        'articles': articles,
        'categories': categories,
        'tags': tags,
        'meta_title': 'Blog - SiraWeb | Actualités Web & SEO Burkina Faso',
        'meta_description': 'Découvrez nos articles sur le développement web, le SEO, le marketing digital et les tendances web au Burkina Faso.',
    }
    return render(request, 'core/blog_list.html', context)


def blog_detail(request, slug):
    """Détail d'un article de blog."""
    article = get_object_or_404(Article, slug=slug, published=True)
    
    # Articles similaires
    similar_articles = Article.objects.filter(
        published=True,
        category=article.category
    ).exclude(id=article.id).order_by('-published_at')[:3]
    
    # Articles récents
    recent_articles = Article.objects.filter(
        published=True
    ).exclude(id=article.id).order_by('-published_at')[:5]
    
    context = {
        'article': article,
        'similar_articles': similar_articles,
        'recent_articles': recent_articles,
        'meta_title': article.meta_title or article.title,
        'meta_description': article.meta_description or article.excerpt,
    }
    return render(request, 'core/blog_detail.html', context)


def blog_category(request, slug):
    """Articles par catégorie."""
    category = get_object_or_404(Category, slug=slug)
    articles_list = Article.objects.filter(published=True, category=category).order_by('-published_at')
    
    paginator = Paginator(articles_list, 9)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'articles': articles,
        'meta_title': f'{category.name} - Blog SiraWeb',
        'meta_description': f'Articles de la catégorie {category.name} sur le blog SiraWeb.',
    }
    return render(request, 'core/blog_category.html', context)


def blog_tag(request, slug):
    """Articles par tag."""
    tag = get_object_or_404(Tag, slug=slug)
    articles_list = Article.objects.filter(published=True, tags=tag).order_by('-published_at')
    
    paginator = Paginator(articles_list, 9)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'articles': articles,
        'meta_title': f'#{tag.name} - Blog SiraWeb',
        'meta_description': f'Articles taggés avec {tag.name} sur le blog SiraWeb.',
    }
    return render(request, 'core/blog_tag.html', context)


def seo_ouagadougou(request):
    """Page SEO Ouagadougou."""
    context = {
        'meta_title': 'SEO Ouagadougou | Référencement Naturel - SiraWeb',
        'meta_description': 'Services de référencement naturel (SEO) à Ouagadougou. SiraWeb vous aide à améliorer votre visibilité sur Google au Burkina Faso.',
    }
    return render(request, 'core/seo_ouagadougou.html', context)


def seo_bobo(request):
    """Page SEO Bobo-Dioulasso."""
    context = {
        'meta_title': 'SEO Bobo-Dioulasso | Référencement Naturel - SiraWeb',
        'meta_description': 'Services de référencement naturel (SEO) à Bobo-Dioulasso. SiraWeb vous aide à améliorer votre visibilité sur Google au Burkina Faso.',
    }
    return render(request, 'core/seo_bobo.html', context)


@require_http_methods(["GET"])
def robots_txt(request):
    """Génère robots.txt."""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /media/",
        "",
        f"Sitemap: {settings.SITE_DOMAIN}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def legal(request):
    """Page Mentions légales."""
    context = {
        'meta_title': 'Mentions Légales - SiraWeb | Agence Web Burkina Faso',
        'meta_description': 'Mentions légales de SiraWeb, agence web au Burkina Faso. Informations sur l\'entreprise, l\'hébergeur et les données personnelles.',
    }
    return render(request, 'core/legal.html', context)


def privacy(request):
    """Page Politique de confidentialité."""
    context = {
        'meta_title': 'Politique de Confidentialité - SiraWeb | Agence Web Burkina Faso',
        'meta_description': 'Politique de confidentialité de SiraWeb. Découvrez comment nous collectons, utilisons et protégeons vos données personnelles.',
    }
    return render(request, 'core/privacy.html', context)


def handler404(request, exception):
    """Page 404 personnalisée."""
    context = {
        'meta_title': '404 - Page non trouvée | SiraWeb',
        'meta_description': 'La page que vous recherchez n\'existe pas ou a été déplacée.',
    }
    return render(request, 'core/404.html', context, status=404)


def handler500(request):
    """Page 500 personnalisée."""
    context = {
        'meta_title': '500 - Erreur serveur | SiraWeb',
        'meta_description': 'Une erreur s\'est produite sur le serveur. Veuillez réessayer plus tard.',
    }
    return render(request, 'core/500.html', context, status=500)


def statistics(request):
    """Page de statistiques du site."""
    from django.db.models import Count, Q
    from django.utils import timezone
    from datetime import timedelta
    from collections import defaultdict
    
    # Vérifier que l'utilisateur est admin
    if not request.user.is_authenticated or not request.user.is_staff:
        from django.contrib.auth.decorators import login_required
        from django.shortcuts import redirect
        return redirect('admin:login')
    
    # Filtrer les visites (exclure les bots)
    views = PageView.objects.filter(is_bot=False)
    
    # Statistiques générales
    total_views = views.count()
    today = timezone.now().date()
    views_today = views.filter(created_at__date=today).count()
    views_this_week = views.filter(created_at__gte=today - timedelta(days=7)).count()
    views_this_month = views.filter(created_at__gte=today - timedelta(days=30)).count()
    views_this_year = views.filter(created_at__gte=today - timedelta(days=365)).count()
    
    # Calculer les variations en pourcentage
    yesterday = today - timedelta(days=1)
    views_yesterday = views.filter(created_at__date=yesterday).count()
    views_last_week = views.filter(created_at__gte=today - timedelta(days=14), created_at__lt=today - timedelta(days=7)).count()
    views_last_month = views.filter(created_at__gte=today - timedelta(days=60), created_at__lt=today - timedelta(days=30)).count()
    
    # Calculer les pourcentages de variation
    if views_yesterday > 0:
        today_variation = ((views_today - views_yesterday) / views_yesterday) * 100
    else:
        today_variation = 100 if views_today > 0 else 0
    
    if views_last_week > 0:
        week_variation = ((views_this_week - views_last_week) / views_last_week) * 100
    else:
        week_variation = 100 if views_this_week > 0 else 0
    
    if views_last_month > 0:
        month_variation = ((views_this_month - views_last_month) / views_last_month) * 100
    else:
        month_variation = 100 if views_this_month > 0 else 0
    
    # Visites par jour (30 derniers jours)
    daily_views = []
    for i in range(29, -1, -1):
        date = today - timedelta(days=i)
        count = views.filter(created_at__date=date).count()
        daily_views.append({
            'date': date.strftime('%Y-%m-%d'),
            'label': date.strftime('%d/%m'),
            'count': count
        })
    
    # Visites par semaine (12 dernières semaines)
    weekly_views = []
    for i in range(11, -1, -1):
        # Calculer le début et la fin de la semaine (lundi à dimanche)
        days_since_monday = today.weekday()  # 0 = lundi, 6 = dimanche
        week_end = today - timedelta(days=days_since_monday) - timedelta(days=i * 7)
        week_start = week_end - timedelta(days=6)
        count = views.filter(created_at__date__gte=week_start, created_at__date__lte=week_end).count()
        weekly_views.append({
            'week': f'Sem {week_start.strftime("%d/%m")}',
            'count': count
        })
    
    # Visites par mois (12 derniers mois)
    monthly_views = []
    for i in range(11, -1, -1):
        # Calculer le début et la fin du mois correctement
        target_date = today - timedelta(days=30 * i)
        month_start = target_date.replace(day=1)
        # Calculer le dernier jour du mois
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1, day=1) - timedelta(days=1)
        count = views.filter(created_at__date__gte=month_start, created_at__date__lte=month_end).count()
        monthly_views.append({
            'month': month_start.strftime('%b %Y'),
            'count': count
        })
    
    # Visites par année
    yearly_views = []
    current_year = today.year
    for year in range(current_year - 4, current_year + 1):
        count = views.filter(created_at__year=year).count()
        yearly_views.append({
            'year': str(year),
            'count': count
        })
    
    # Répartition par pays
    country_stats = views.exclude(country_code='').values('country', 'country_code').annotate(
        count=Count('id')
    ).order_by('-count')[:20]
    
    country_data = [{'country': item['country'] or 'Inconnu', 'code': item['country_code'], 'count': item['count']} 
                    for item in country_stats]
    
    # Pages les plus visitées
    top_pages = list(views.values('path').annotate(count=Count('id')).order_by('-count')[:10])
    
    # Convertir en JSON pour le template
    import json
    context = {
        'meta_title': 'Statistiques du site | SiraWeb',
        'meta_description': 'Tableau de bord des statistiques de visite du site.',
        'total_views': total_views,
        'views_today': views_today,
        'views_this_week': views_this_week,
        'views_this_month': views_this_month,
        'views_this_year': views_this_year,
        'today_variation': round(today_variation, 2),
        'week_variation': round(week_variation, 2),
        'month_variation': round(month_variation, 2),
        'daily_views': json.dumps(daily_views),
        'weekly_views': json.dumps(weekly_views),
        'monthly_views': json.dumps(monthly_views),
        'yearly_views': json.dumps(yearly_views),
        'country_data': json.dumps(country_data),
        'top_pages': json.dumps(top_pages),
    }
    return render(request, 'core/statistics.html', context)
