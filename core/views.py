from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import Article, Category, Tag, Service, TeamMember, Testimonial, Partner, Portfolio
from .forms import ContactForm


def home(request):
    """Page d'accueil."""
    testimonials = Testimonial.objects.filter(active=True).order_by('order')[:6]
    partners = Partner.objects.filter(active=True).order_by('order')[:8]
    portfolio_projects = Portfolio.objects.filter(active=True).order_by('order')[:4]
    
    context = {
        'testimonials': testimonials,
        'partners': partners,
        'portfolio_projects': portfolio_projects,
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
    
    context = {
        'team_members': team_members,
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
    return render(request, 'core/404.html', status=404)


def handler500(request):
    """Page 500 personnalisée."""
    return render(request, 'core/500.html', status=500)
