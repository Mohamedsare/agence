from django.urls import path
from . import views

urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    path('services/', views.services_list, name='services_list'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('agence/', views.about, name='about'),
    path('agence/equipe/', views.team, name='team'),
    path('contact/', views.contact, name='contact'),
    
    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/categorie/<slug:slug>/', views.blog_category, name='blog_category'),
    path('blog/tag/<slug:slug>/', views.blog_tag, name='blog_tag'),
    
    # Pages SEO locales
    path('seo-ouagadougou/', views.seo_ouagadougou, name='seo_ouagadougou'),
    path('seo-bobo-dioulasso/', views.seo_bobo, name='seo_bobo'),
    
    # Pages légales
    path('mentions-legales/', views.legal, name='legal'),
    path('politique-de-confidentialite/', views.privacy, name='privacy'),
    
    # Statistiques
    path('statistiques/', views.statistics, name='statistics'),
    
    # Robots.txt
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
