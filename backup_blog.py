#!/usr/bin/env python
"""
Script de sauvegarde/restauration des articles de blog
Usage:
    python backup_blog.py export    # Exporter les articles
    python backup_blog.py import    # Importer les articles
"""
import os
import sys
import django
import json
from pathlib import Path
from datetime import datetime

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siraweb.settings')
django.setup()

from core.models import Article, Category, Tag
from django.utils import timezone


def export_blog():
    """Exporter tous les articles de blog vers un fichier JSON."""
    articles = Article.objects.all().select_related('category').prefetch_related('tags')
    data = {
        'articles': [],
        'categories': [],
        'tags': [],
        'export_date': timezone.now().isoformat()
    }
    
    # Exporter les catégories
    categories = Category.objects.all()
    for category in categories:
        data['categories'].append({
            'name': category.name,
            'slug': category.slug,
            'description': category.description,
        })
    
    # Exporter les tags
    tags = Tag.objects.all()
    for tag in tags:
        data['tags'].append({
            'name': tag.name,
            'slug': tag.slug,
        })
    
    # Exporter les articles
    for article in articles:
        article_data = {
            'title': article.title,
            'slug': article.slug,
            'excerpt': article.excerpt,
            'content': article.content,
            'author': article.author,
            'published': article.published,
            'published_at': article.published_at.isoformat() if article.published_at else None,
            'meta_title': article.meta_title,
            'meta_description': article.meta_description,
            'category': article.category.slug if article.category else None,
            'tags': [tag.slug for tag in article.tags.all()],
        }
        data['articles'].append(article_data)
    
    output_file = BASE_DIR / 'blog_backup.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] {len(data['articles'])} article(s) exporte(s)")
    print(f"[OK] {len(data['categories'])} categorie(s) exportee(s)")
    print(f"[OK] {len(data['tags'])} tag(s) exporte(s)")
    print(f"[OK] Sauvegarde vers {output_file}")
    return output_file


def import_blog():
    """Importer les articles de blog depuis un fichier JSON."""
    input_file = BASE_DIR / 'blog_backup.json'
    
    if not input_file.exists():
        print(f"[ERREUR] Fichier {input_file} introuvable!")
        return
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Importer les catégories
    categories_created = 0
    categories_map = {}
    for cat_data in data.get('categories', []):
        category, created = Category.objects.update_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data.get('description', ''),
            }
        )
        categories_map[cat_data['slug']] = category
        if created:
            categories_created += 1
    
    # Importer les tags
    tags_created = 0
    tags_map = {}
    for tag_data in data.get('tags', []):
        tag, created = Tag.objects.update_or_create(
            slug=tag_data['slug'],
            defaults={
                'name': tag_data['name'],
            }
        )
        tags_map[tag_data['slug']] = tag
        if created:
            tags_created += 1
    
    # Importer les articles
    articles_created = 0
    articles_updated = 0
    
    for article_data in data.get('articles', []):
        # Gérer la date de publication
        published_at = None
        if article_data.get('published_at'):
            try:
                published_at = timezone.datetime.fromisoformat(article_data['published_at'].replace('Z', '+00:00'))
            except:
                published_at = None
        
        article, created = Article.objects.update_or_create(
            slug=article_data['slug'],
            defaults={
                'title': article_data['title'],
                'excerpt': article_data.get('excerpt', ''),
                'content': article_data.get('content', ''),
                'author': article_data.get('author', 'FASOWEB'),
                'published': article_data.get('published', False),
                'published_at': published_at,
                'meta_title': article_data.get('meta_title', ''),
                'meta_description': article_data.get('meta_description', ''),
                'category': categories_map.get(article_data.get('category')) if article_data.get('category') else None,
            }
        )
        
        # Ajouter les tags
        if article_data.get('tags'):
            article.tags.clear()
            for tag_slug in article_data['tags']:
                if tag_slug in tags_map:
                    article.tags.add(tags_map[tag_slug])
        
        if created:
            articles_created += 1
            print(f"[OK] Article cree: {article.title}")
        else:
            articles_updated += 1
            print(f"[UPDATE] Article mis a jour: {article.title}")
    
    print(f"\n[SUCCESS] Termine !")
    print(f"  - {categories_created} categorie(s) creee(s)")
    print(f"  - {tags_created} tag(s) cree(s)")
    print(f"  - {articles_created} article(s) cree(s), {articles_updated} article(s) mis a jour")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python backup_blog.py [export|import]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'export':
        export_blog()
    elif command == 'import':
        import_blog()
    else:
        print("Commande invalide. Utilisez 'export' ou 'import'")
        sys.exit(1)
