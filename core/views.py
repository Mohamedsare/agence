import json
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import Article, Category, Tag, Service, TeamMember, Testimonial, Partner, Portfolio, Technology, AnonymousCTA, FAQ, CompanyStats, PageView, AssistantQuestion, ContactMessage, PageBanner
from .forms import ContactForm

# Prompt système pour l'assistant FASOWEB (DeepSeek) - orienté conversion
ASSISTANT_SYSTEM_PROMPT = """Tu es l'assistant commercial de FASOWEB, agence web au Burkina Faso (Ouagadougou, Bobo-Dioulasso). Ton objectif : aider au maximum ET convertir les visiteurs en clients.

Ton rôle :
- Répondre à toutes les questions : sites vitrine, e-commerce, SEO, refonte, maintenance, tarifs, délais, processus.
- Donner des fourchettes de prix indicatives quand on te demande : site vitrine (souvent entre 200 000 et 800 000 FCFA selon la complexité), e-commerce (à partir d’environ 500 000 FCFA), SEO / accompagnement (forfaits selon objectifs). Toujours préciser que ces montants sont indicatifs et qu’un devis gratuit permet un chiffrage précis.
- Rappeler que l’accompagnement FASOWEB est continu et illimité après livraison : support, conseils, évolutions, pas de limite dans le temps pour nos clients.
- Inciter à nous contacter pour un devis personnalisé : formulaire sur le site, WhatsApp, email, téléphone. Proposer d’ouvrir le formulaire de devis ou de discuter sur WhatsApp pour aller plus loin.

Règles : Réponds en français, concis et chaleureux. À la fin de CHAQUE réponse, invite à cliquer sur « Demander un devis gratuit » ou « Écrire sur WhatsApp » en bas du chat. Chaque réponse doit aider ET inciter à passer à l'action."""


def home(request):
    """Page d'accueil."""
    testimonials = Testimonial.objects.filter(active=True).order_by('order')[:6]
    partners = Partner.objects.filter(active=True).order_by('order')[:8]
    portfolio_projects = Portfolio.objects.filter(active=True).order_by('order')
    technologies = Technology.objects.filter(active=True).order_by('order', 'name')
    services = Service.objects.filter(active=True).order_by('order', 'name')[:6]
    anonymous_cta = AnonymousCTA.objects.filter(active=True).first()
    banner_images = PageBanner.objects.filter(page='home').order_by('order')
    
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
        'banner_images': banner_images,
        'meta_title': 'FASOWEB - Agence Web au Burkina Faso | Création de Sites Web Modernes',
        'meta_description': 'Agence web au Burkina Faso spécialisée dans la création de sites web sur mesure, SEO et développement web moderne. Services à Ouagadougou et Bobo-Dioulasso.',
    }
    return render(request, 'core/home.html', context)


def services_list(request):
    """Liste des services."""
    services = Service.objects.filter(active=True).order_by('order', 'name')
    company_stats = CompanyStats.objects.filter(active=True).first()
    
    context = {
        'services': services,
        'company_stats': company_stats,
        'meta_title': 'Services Web au Burkina Faso | Création site, SEO, E-commerce | FASOWEB Ouagadougou',
        'meta_description': 'Agence web Burkina Faso : création de sites vitrine, e-commerce, SEO, refonte, maintenance à Ouagadougou et Bobo-Dioulasso. Devis gratuit sous 24h. +50 projets réalisés.',
    }
    return render(request, 'core/services_list.html', context)


def service_detail(request, slug):
    """Détail d'un service."""
    service = get_object_or_404(Service, slug=slug, active=True)
    similar_services = Service.objects.filter(active=True).exclude(id=service.id).order_by('order')[:3]
    banner_images = PageBanner.objects.filter(page='services').order_by('order')
    service_name = service.get_name_display()
    meta_title = service.meta_title or f'{service_name} au Burkina Faso | FASOWEB Agence Web Ouagadougou'
    meta_description = service.meta_description or service.short_description
    if len(meta_description) < 100 and 'Burkina' not in meta_description:
        meta_description = f'{meta_description} Service proposé par FASOWEB à Ouagadougou et Bobo-Dioulasso. Devis gratuit.'
    context = {
        'service': service,
        'similar_services': similar_services,
        'banner_images': banner_images,
        'meta_title': meta_title,
        'meta_description': meta_description,
    }
    return render(request, 'core/service_detail.html', context)


def maintenance_page(request):
    """Page dédiée Maintenance de site web (même bannière slider que les autres pages Services)."""
    similar_services = Service.objects.filter(active=True).order_by('order')[:3]
    banner_images = PageBanner.objects.filter(page='services').order_by('order')
    context = {
        'similar_services': similar_services,
        'banner_images': banner_images,
        'meta_title': 'Maintenance de site web Burkina Faso | Ouagadougou, Bobo | FASOWEB',
        'meta_description': 'Maintenance et hébergement de sites web au Burkina Faso. Mises à jour, sauvegardes, sécurité. Ouagadougou & Bobo-Dioulasso. Devis gratuit.',
    }
    return render(request, 'core/maintenance.html', context)


def about(request):
    """Page À propos."""
    team_members = TeamMember.objects.filter(active=True).order_by('order', 'name')
    company_stats = CompanyStats.objects.filter(active=True).first()
    
    context = {
        'team_members': team_members,
        'company_stats': company_stats,
        'meta_title': 'À Propos - FASOWEB | Agence Web Burkina Faso',
        'meta_description': 'Découvrez FASOWEB, votre agence web au Burkina Faso. Notre équipe experte vous accompagne dans vos projets web à Ouagadougou et Bobo-Dioulasso.',
    }
    return render(request, 'core/about.html', context)


def team(request):
    """Page Équipe."""
    team_members = TeamMember.objects.filter(active=True).order_by('order', 'name')
    
    context = {
        'team_members': team_members,
        'meta_title': 'Notre Équipe - FASOWEB | Agence Web Burkina Faso',
        'meta_description': 'Rencontrez l\'équipe FASOWEB, des experts en développement web, SEO et design UI/UX au Burkina Faso.',
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
        'meta_title': 'Contact - FASOWEB | Agence Web Burkina Faso',
        'meta_description': 'Contactez FASOWEB pour vos projets web au Burkina Faso. Devis gratuit pour création de site web, SEO, refonte à Ouagadougou et Bobo-Dioulasso.',
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
        'meta_title': 'Blog - FASOWEB | Actualités Web & SEO Burkina Faso',
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
        'meta_title': f'{category.name} - Blog FASOWEB',
        'meta_description': f'Articles de la catégorie {category.name} sur le blog FASOWEB.',
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
        'meta_title': f'#{tag.name} - Blog FASOWEB',
        'meta_description': f'Articles taggés avec {tag.name} sur le blog FASOWEB.',
    }
    return render(request, 'core/blog_tag.html', context)


def seo_ouagadougou(request):
    """Page SEO Ouagadougou."""
    context = {
        'meta_title': 'SEO Ouagadougou | Référencement Naturel - FASOWEB',
        'meta_description': 'Services de référencement naturel (SEO) à Ouagadougou. FASOWEB vous aide à améliorer votre visibilité sur Google au Burkina Faso.',
    }
    return render(request, 'core/seo_ouagadougou.html', context)


def seo_bobo(request):
    """Page SEO Bobo-Dioulasso."""
    context = {
        'meta_title': 'SEO Bobo-Dioulasso | Référencement Naturel - FASOWEB',
        'meta_description': 'Services de référencement naturel (SEO) à Bobo-Dioulasso. FASOWEB vous aide à améliorer votre visibilité sur Google au Burkina Faso.',
    }
    return render(request, 'core/seo_bobo.html', context)


@require_http_methods(["GET"])
def robots_txt(request):
    """Génère robots.txt."""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /statistiques/",
        "Disallow: /media/",
        "",
        f"Sitemap: {settings.SITE_DOMAIN}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def legal(request):
    """Page Mentions légales."""
    context = {
        'meta_title': 'Mentions Légales - FASOWEB | Agence Web Burkina Faso',
        'meta_description': 'Mentions légales de FASOWEB, agence web au Burkina Faso. Informations sur l\'entreprise, l\'hébergeur et les données personnelles.',
    }
    return render(request, 'core/legal.html', context)


def privacy(request):
    """Page Politique de confidentialité."""
    context = {
        'meta_title': 'Politique de Confidentialité - FASOWEB | Agence Web Burkina Faso',
        'meta_description': 'Politique de confidentialité de FASOWEB. Découvrez comment nous collectons, utilisons et protégeons vos données personnelles.',
    }
    return render(request, 'core/privacy.html', context)


def handler404(request, exception):
    """Page 404 personnalisée."""
    context = {
        'meta_title': '404 - Page non trouvée | FASOWEB',
        'meta_description': 'La page que vous recherchez n\'existe pas ou a été déplacée.',
    }
    return render(request, 'core/404.html', context, status=404)


def handler500(request):
    """Page 500 personnalisée."""
    context = {
        'meta_title': '500 - Erreur serveur | FASOWEB',
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
    
    # Répartition par type d'appareil (pour camembert)
    device_stats = views.values('device_type').annotate(count=Count('id')).order_by('-count')
    device_labels = dict(PageView.DEVICE_CHOICES)
    device_data = [{'label': device_labels.get(item['device_type'], item['device_type']), 'count': item['count']} 
                   for item in device_stats]
    
    # Pages les plus visitées
    top_pages = list(views.values('path').annotate(count=Count('id')).order_by('-count')[:10])

    # Dernières questions posées à l'assistant (tableau de bord)
    assistant_questions = AssistantQuestion.objects.all().order_by('-created_at')[:100]
    
    # Dernières visites (date/heure, page, provenance, pays/ville)
    last_visits = views.order_by('-created_at')[:100]
    
    # Convertir en JSON pour le template
    import json
    context = {
        'meta_title': 'Statistiques du site | FASOWEB',
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
        'device_data': json.dumps(device_data),
        'top_pages': json.dumps(top_pages),
        'assistant_questions': assistant_questions,
        'last_visits': last_visits,
    }
    return render(request, 'core/statistics.html', context)


def statistics_realtime(request):
    """
    API JSON pour le rafraîchissement temps réel du tableau de bord :
    dernières visites et données pays (carte). Réservé aux staff.
    """
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    from django.db.models import Count
    views = PageView.objects.filter(is_bot=False)
    # Dernières visites (100)
    last = views.order_by('-created_at')[:100]
    last_visits = [
        {
            'created_at': v.created_at.strftime('%d/%m/%Y %H:%M'),
            'path': v.path[:50] + ('…' if len(v.path) > 50 else ''),
            'referer': v.referer or '',
            'country': v.country or '',
            'city': v.city or '',
            'device': v.get_device_type_display(),
        }
        for v in last
    ]
    # Répartition par pays (carte)
    country_stats = views.exclude(country_code='').values('country', 'country_code').annotate(
        count=Count('id')
    ).order_by('-count')[:20]
    country_data = [
        {'country': item['country'] or 'Inconnu', 'code': item['country_code'], 'count': item['count']}
        for item in country_stats
    ]
    return JsonResponse({'last_visits': last_visits, 'country_data': country_data})


def dashboard_messages(request):
    """Page Messages du tableau de bord : contact, demandes de devis."""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin:login')
    contact_messages = ContactMessage.objects.all().order_by('-created_at')[:200]
    context = {
        'contact_messages': contact_messages,
    }
    return render(request, 'core/dashboard_messages.html', context)


@require_http_methods(['POST'])
def assistant_chat(request):
    """
    Endpoint API pour le chat de l'assistant FASOWEB (DeepSeek).
    Body JSON : { "message": "..." } ou { "messages": [ { "role": "user", "content": "..." } ] }.
    Si "message" est fourni, on l'ajoute à l'historique ; "messages" permet d'envoyer tout l'historique.
    """
    api_key = getattr(settings, 'DEEPSEEK_API_KEY', None)
    if not api_key:
        return JsonResponse(
            {'error': 'L’assistant n’est pas configuré pour le moment. Contactez-nous par le formulaire ou WhatsApp.'},
            status=503
        )

    try:
        body = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Requête invalide.'}, status=400)

    # Construire la liste des messages pour DeepSeek
    messages_for_api = [{'role': 'system', 'content': ASSISTANT_SYSTEM_PROMPT}]

    if 'messages' in body and isinstance(body['messages'], list):
        for m in body['messages']:
            if isinstance(m, dict) and m.get('role') in ('user', 'assistant') and m.get('content'):
                messages_for_api.append({'role': m['role'], 'content': m['content']})
    elif body.get('message'):
        messages_for_api.append({'role': 'user', 'content': str(body['message']).strip()})
    else:
        return JsonResponse({'error': 'Message manquant.'}, status=400)

    if not any(m.get('role') == 'user' for m in messages_for_api[1:]):
        return JsonResponse({'error': 'Aucun message utilisateur.'}, status=400)

    # Enregistrer la dernière question utilisateur pour le tableau de bord
    try:
        last_user_msg = next((m.get('content', '') for m in reversed(messages_for_api[1:]) if m.get('role') == 'user'), '')
        if last_user_msg and last_user_msg.strip():
            AssistantQuestion.objects.create(content=last_user_msg.strip())
    except Exception:
        pass

    payload = {
        'model': 'deepseek-chat',
        'messages': messages_for_api,
        'max_tokens': 1024,
        'temperature': 0.7,
    }

    try:
        api_url = getattr(settings, 'DEEPSEEK_API_URL', 'https://api.deepseek.com/v1/chat/completions')
        r = requests.post(
            api_url,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
            json=payload,
            timeout=60,
        )
        r.raise_for_status()
        data = r.json()
    except requests.HTTPError as e:
        # Erreur HTTP (401, 429, 500...) : récupérer le détail si possible
        try:
            err_body = e.response.json() if e.response else {}
            err_msg = err_body.get('error', {}).get('message', str(e)) if isinstance(err_body.get('error'), dict) else str(e)
        except Exception:
            err_msg = str(e)
        if settings.DEBUG:
            return JsonResponse({
                'error': f'Erreur API DeepSeek ({e.response.status_code if e.response else "?"}): {err_msg}. Contactez-nous si le problème persiste.'
            }, status=502)
        return JsonResponse(
            {'error': 'Service temporairement indisponible. Vous pouvez nous contacter directement.'},
            status=502
        )
    except requests.RequestException as e:
        if settings.DEBUG:
            return JsonResponse({
                'error': f'Connexion impossible: {str(e)}. Vérifiez votre connexion ou réessayez plus tard.'
            }, status=502)
        return JsonResponse(
            {'error': 'Service temporairement indisponible. Vous pouvez nous contacter directement.'},
            status=502
        )

    choice = (data.get('choices') or [None])[0]
    if not choice or 'message' not in choice:
        return JsonResponse({'error': 'Réponse invalide du service.'}, status=502)

    content = (choice.get('message') or {}).get('content') or ''
    return JsonResponse({'content': content})
