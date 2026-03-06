#!/usr/bin/env python
"""
Script de restauration des données de test FASOWEB.
À exécuter sur le serveur : python restore.py [--reset]

Restaure : FAQs, Projets (Portfolio), Services, Blog (catégories, tags, articles).

Sans --reset : crée ou met à jour les données (get_or_create / update_or_create).
Avec --reset : supprime toutes les données de test puis les recrée.
"""
import os
import sys
import argparse
from io import BytesIO
from datetime import timedelta

# Configuration Django (à lancer depuis la racine du projet)
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siraweb.settings_deploy")
    import django
    django.setup()

from django.utils import timezone
from django.core.files.base import ContentFile
from core.models import (
    FAQ,
    Portfolio,
    Service,
    Article,
    Category,
    Tag,
)


def make_placeholder_image():
    """Génère une image placeholder pour les projets portfolio (sans fichier externe)."""
    try:
        from PIL import Image
        img = Image.new("RGB", (800, 500), color=(240, 240, 245))
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=85)
        return ContentFile(buf.getvalue(), name="placeholder.jpg")
    except Exception:
        return None


def delete_test_data():
    """Supprime toutes les données de test (ordre respectant les clés étrangères)."""
    Article.objects.all().delete()
    FAQ.objects.all().delete()
    Portfolio.objects.all().delete()
    Service.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    print("  Données de test supprimées.")


def create_services():
    """Crée ou met à jour tous les services."""
    data = [
        {"name": "vitrine", "short_description": "Création de sites vitrine modernes et performants pour mettre en valeur votre entreprise.", "full_description": "Nous créons des sites vitrine sur mesure qui reflètent l'identité de votre entreprise. Design moderne, responsive et optimisé pour le SEO.", "meta_title": "Création de Site Vitrine - FASOWEB Burkina Faso", "meta_description": "Création de sites vitrine modernes et performants au Burkina Faso.", "order": 1},
        {"name": "ecommerce", "short_description": "Développement de boutiques en ligne complètes avec gestion des commandes et paiements.", "full_description": "Solutions e-commerce complètes pour vendre vos produits en ligne. Interface intuitive, gestion des stocks, paiements sécurisés.", "meta_title": "Site E-commerce Burkina Faso - FASOWEB", "meta_description": "Création de boutiques en ligne au Burkina Faso.", "order": 2},
        {"name": "institutionnel", "short_description": "Sites institutionnels pour les organisations, administrations et structures publiques.", "full_description": "Sites web institutionnels professionnels : accessibilité, conformité, contenu structuré. Idéal pour le secteur public au Burkina Faso.", "meta_title": "Site Institutionnel - FASOWEB Burkina Faso", "meta_description": "Création de sites institutionnels au Burkina Faso.", "order": 3},
        {"name": "landing", "short_description": "Landing pages percutantes pour vos campagnes marketing et génération de leads.", "full_description": "Pages d'atterrissage optimisées pour la conversion : formulaire, CTA, suivi des performances.", "meta_title": "Landing Pages - FASOWEB Burkina Faso", "meta_description": "Création de landing pages au Burkina Faso.", "order": 4},
        {"name": "refonte", "short_description": "Refonte UI/UX de votre site pour un design moderne et de meilleures performances.", "full_description": "Nous modernisons votre site existant : nouveau design, UX, technique à jour.", "meta_title": "Refonte UI/UX - FASOWEB Burkina Faso", "meta_description": "Refonte de sites web au Burkina Faso.", "order": 5},
        {"name": "seo", "short_description": "Optimisation SEO pour améliorer votre visibilité sur Google au Burkina Faso.", "full_description": "Services de référencement naturel (SEO) pour améliorer votre positionnement.", "meta_title": "SEO Burkina Faso - FASOWEB", "meta_description": "Services SEO au Burkina Faso.", "order": 6},
        {"name": "sea", "short_description": "Campagnes Google Ads (SEA) pour une visibilité immédiate et des leads qualifiés.", "full_description": "Gestion de campagnes Google Ads : search, display, remarketing. Ciblage et suivi des conversions.", "meta_title": "SEA Google Ads - FASOWEB Burkina Faso", "meta_description": "Campagnes Google Ads (SEA) au Burkina Faso.", "order": 7},
        {"name": "maintenance", "short_description": "Maintenance technique, mises à jour et hébergement pour garder votre site rapide et sécurisé.", "full_description": "Maintenance de site web, mises à jour de sécurité et de contenu, hébergement fiable.", "meta_title": "Maintenance de site web - FASOWEB Burkina Faso", "meta_description": "Maintenance et hébergement de sites web au Burkina Faso.", "order": 8, "slug": "maintenance-site-web"},
    ]
    for item in data:
        slug = item.pop("slug", None)
        name = item.pop("name")
        defaults = dict(item)
        if slug is not None:
            defaults["slug"] = slug
        Service.objects.get_or_create(name=name, defaults=defaults)
    print("  Services : OK")


def create_categories_and_tags():
    """Crée catégories et tags du blog. Retourne (categories, tags)."""
    categories_data = [
        {"name": "Développement Web", "description": "Articles sur le développement web et les technologies"},
        {"name": "SEO", "description": "Conseils et actualités sur le référencement naturel"},
        {"name": "Design UI/UX", "description": "Tendances et bonnes pratiques en design"},
        {"name": "Marketing Digital", "description": "Stratégies et outils de marketing digital"},
    ]
    categories = []
    for d in categories_data:
        c, _ = Category.objects.get_or_create(name=d["name"], defaults={"description": d["description"]})
        categories.append(c)
    tags_data = ["Django", "Python", "SEO", "Burkina Faso", "Web Design", "Performance", "Mobile", "E-commerce"]
    tags = []
    for name in tags_data:
        t, _ = Tag.objects.get_or_create(name=name)
        tags.append(t)
    print("  Catégories et tags : OK")
    return categories, tags


def create_articles(categories, tags):
    """Crée les articles de blog de test."""
    now = timezone.now()
    articles_data = [
        {"title": "Pourquoi avoir un site web en 2026 au Burkina Faso ?", "excerpt": "Découvrez pourquoi il est essentiel pour votre entreprise d'avoir une présence en ligne.", "content": "Le digital prend de plus en plus d'importance au Burkina Faso. Avoir un site web devient indispensable pour votre entreprise. Les consommateurs recherchent les produits et services en ligne.", "category": categories[0] if categories else None, "tags": tags[:3], "published_at": now - timedelta(days=5)},
        {"title": "Les 5 erreurs SEO à éviter pour votre site web", "excerpt": "Évitez ces erreurs courantes qui nuisent au référencement de votre site.", "content": "Le SEO est crucial pour la visibilité. Erreurs à éviter : ignorer la vitesse, négliger le mobile, oublier les balises meta, dupliquer le contenu, ignorer les backlinks.", "category": categories[1] if len(categories) > 1 else None, "tags": tags[2:5], "published_at": now - timedelta(days=10)},
        {"title": "Comment créer un site e-commerce performant au Burkina Faso", "excerpt": "Guide pour lancer votre boutique en ligne au Burkina Faso.", "content": "Créer un site e-commerce au Burkina Faso nécessite une approche adaptée : moyens de paiement, logistique, habitudes des consommateurs.", "category": categories[0] if categories else None, "tags": tags[4:7] if len(tags) > 6 else tags[:3], "published_at": now - timedelta(days=15)},
        {"title": "Tendances design web 2026", "excerpt": "Découvrez les tendances design qui vont dominer le web en 2026.", "content": "Interfaces minimalistes, animations subtiles, couleurs audacieuses, accent sur l'accessibilité.", "category": categories[2] if len(categories) > 2 else None, "tags": tags[5:8] if len(tags) > 7 else tags[:3], "published_at": now - timedelta(days=20)},
        {"title": "Marketing digital au Burkina Faso : stratégies efficaces", "excerpt": "Stratégies de marketing digital adaptées au marché burkinabè.", "content": "Le marketing digital au Burkina Faso présente des opportunités uniques. Smartphones et réseaux sociaux permettent d'atteindre l'audience de manière ciblée.", "category": categories[3] if len(categories) > 3 else None, "tags": tags[3:6] if len(tags) > 5 else tags[:3], "published_at": now - timedelta(days=25)},
    ]
    for d in articles_data:
        tags_list = d.pop("tags", [])
        defaults = {
            "excerpt": d["excerpt"][:300],
            "content": d["content"],
            "category": d.get("category"),
            "published": True,
            "published_at": d.get("published_at"),
            "meta_title": d["title"][:65],
            "meta_description": d["excerpt"][:160],
        }
        article, created = Article.objects.get_or_create(title=d["title"], defaults=defaults)
        if created:
            article.tags.set(tags_list)
    print("  Articles blog : OK")


def create_faqs():
    """Crée les FAQs de test."""
    faqs_data = [
        {"question": "Qui est FASOWEB ?", "answer": "FASOWEB est une agence web spécialisée dans la création de sites web modernes, performants et optimisés SEO, dédiée aux entreprises au Burkina Faso et en Afrique francophone.", "order": 1},
        {"question": "Quels types de sites proposez-vous ?", "answer": "Sites vitrines, e-commerce, institutionnels, landing pages, refontes. Tous responsive et optimisés SEO.", "order": 2},
        {"question": "Les sites sont-ils compatibles mobile ?", "answer": "Oui. Tous nos sites sont 100 % responsive (mobile-first).", "order": 3},
        {"question": "Proposez-vous le SEO ?", "answer": "Oui. Chaque site est conçu avec une structure SEO optimisée et un chargement rapide.", "order": 4},
        {"question": "Pouvez-vous gérer la maintenance ?", "answer": "Oui. Nous proposons des formules de maintenance : mises à jour, sécurité, sauvegardes, assistance.", "order": 5},
        {"question": "Combien de temps pour créer un site ?", "answer": "Site vitrine : 7 à 14 jours. Site e-commerce : 14 à 30 jours (selon complexité).", "order": 6},
        {"question": "Quels sont vos tarifs ?", "answer": "Nos tarifs dépendent du type de site et des fonctionnalités. Nous proposons des prix accessibles et transparents, adaptés au marché burkinabè.", "order": 7},
        {"question": "Les devis sont-ils gratuits ?", "answer": "Oui, 100 % gratuits et sans engagement.", "order": 8},
        {"question": "Comment vous contacter ?", "answer": "Via le formulaire de contact, WhatsApp ou email professionnel.", "order": 9},
        {"question": "Comment démarrer avec FASOWEB ?", "answer": "Il suffit de nous contacter. Nous nous occupons du reste.", "order": 10},
    ]
    for d in faqs_data:
        FAQ.objects.update_or_create(question=d["question"], defaults={"answer": d["answer"], "order": d["order"], "active": True})
    print("  FAQs : OK")


def create_portfolio():
    """Crée les projets portfolio de test (avec image placeholder si possible)."""
    data = [
        {"name": "Site vitrine Entreprise XYZ", "company": "Entreprise XYZ", "category": "vitrine", "description": "Site vitrine moderne pour une entreprise burkinabè.", "order": 1},
        {"name": "Boutique en ligne Moda", "company": "Boutique Moda", "category": "ecommerce", "description": "E-commerce de vêtements et accessoires.", "order": 2},
        {"name": "Portail institutionnel", "company": "Organisation Partenaire", "category": "institutionnel", "description": "Site institutionnel responsive et accessible.", "order": 3},
    ]
    if not make_placeholder_image():
        print("  Portfolio : ignoré (Pillow requis pour l'image placeholder)")
        return
    for d in data:
        defaults = {
            "company": d.get("company", ""),
            "description": d.get("description", ""),
            "category": d.get("category", "vitrine"),
            "order": d.get("order", 0),
            "active": True,
            "image": make_placeholder_image(),  # nouveau fichier à chaque fois
        }
        obj, created = Portfolio.objects.get_or_create(name=d["name"], defaults=defaults)
    print("  Portfolio (projets) : OK")


def main():
    parser = argparse.ArgumentParser(description="Restaure toutes les données de test (FAQs, projets, services, blog).")
    parser.add_argument("--reset", action="store_true", help="Supprimer toutes les données de test avant de les recréer.")
    args = parser.parse_args()

    print("Restauration des données de test FASOWEB...")
    if args.reset:
        delete_test_data()

    create_services()
    categories, tags = create_categories_and_tags()
    create_articles(categories, tags)
    create_faqs()
    create_portfolio()

    print("Terminé. Données de test restaurées.")


if __name__ == "__main__":
    main()
