"""
Command Django pour créer des données de démonstration.
Usage: python manage.py create_demo_data
"""
from django.core.management.base import BaseCommand
from core.models import (
    Service, Article, Category, Tag, TeamMember,
    Testimonial, Partner
)


class Command(BaseCommand):
    help = 'Crée des données de démonstration pour le site SiraWeb'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Création des données de démonstration...'))

        # Services
        self.create_services()
        
        # Catégories et Tags
        categories = self.create_categories()
        tags = self.create_tags()
        
        # Articles
        self.create_articles(categories, tags)
        
        # Équipe
        self.create_team()
        
        # Témoignages
        self.create_testimonials()
        
        # Partenaires
        self.create_partners()

        self.stdout.write(self.style.SUCCESS('✓ Données de démonstration créées avec succès!'))

    def create_services(self):
        """Crée les services de base."""
        services_data = [
            {
                'name': 'vitrine',
                'short_description': 'Création de sites vitrine modernes et performants pour mettre en valeur votre entreprise.',
                'full_description': 'Nous créons des sites vitrine sur mesure qui reflètent l\'identité de votre entreprise. Design moderne, responsive et optimisé pour le SEO.',
                'meta_title': 'Création de Site Vitrine - SiraWeb Burkina Faso',
                'meta_description': 'Création de sites vitrine modernes et performants au Burkina Faso. Design sur mesure, responsive et SEO-friendly.',
                'order': 1
            },
            {
                'name': 'ecommerce',
                'short_description': 'Développement de boutiques en ligne complètes avec gestion des commandes et paiements.',
                'full_description': 'Solutions e-commerce complètes pour vendre vos produits en ligne. Interface intuitive, gestion des stocks, paiements sécurisés.',
                'meta_title': 'Site E-commerce Burkina Faso - SiraWeb',
                'meta_description': 'Création de boutiques en ligne au Burkina Faso. Solutions e-commerce complètes avec gestion des commandes.',
                'order': 2
            },
            {
                'name': 'seo',
                'short_description': 'Optimisation SEO pour améliorer votre visibilité sur Google au Burkina Faso.',
                'full_description': 'Services de référencement naturel (SEO) pour améliorer votre positionnement sur les moteurs de recherche.',
                'meta_title': 'SEO Burkina Faso - Référencement Naturel SiraWeb',
                'meta_description': 'Services SEO au Burkina Faso. Améliorez votre visibilité sur Google avec notre expertise en référencement naturel.',
                'order': 6
            },
        ]

        for data in services_data:
            service, created = Service.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  ✓ Service créé: {service.get_name_display()}')

    def create_categories(self):
        """Crée les catégories du blog."""
        categories_data = [
            {'name': 'Développement Web', 'description': 'Articles sur le développement web et les technologies'},
            {'name': 'SEO', 'description': 'Conseils et actualités sur le référencement naturel'},
            {'name': 'Design UI/UX', 'description': 'Tendances et bonnes pratiques en design'},
            {'name': 'Marketing Digital', 'description': 'Stratégies et outils de marketing digital'},
        ]

        categories = []
        for data in categories_data:
            cat, created = Category.objects.get_or_create(
                name=data['name'],
                defaults={'description': data['description']}
            )
            categories.append(cat)
            if created:
                self.stdout.write(f'  ✓ Catégorie créée: {cat.name}')

        return categories

    def create_tags(self):
        """Crée les tags du blog."""
        tags_data = ['Django', 'Python', 'SEO', 'Burkina Faso', 'Web Design', 'Performance', 'Mobile', 'E-commerce']

        tags = []
        for name in tags_data:
            tag, created = Tag.objects.get_or_create(name=name)
            tags.append(tag)
            if created:
                self.stdout.write(f'  ✓ Tag créé: {tag.name}')

        return tags

    def create_articles(self, categories, tags):
        """Crée des articles de blog de démonstration."""
        from django.utils import timezone
        from datetime import timedelta

        articles_data = [
            {
                'title': 'Pourquoi avoir un site web en 2026 au Burkina Faso ?',
                'excerpt': 'Découvrez pourquoi il est essentiel pour votre entreprise d\'avoir une présence en ligne au Burkina Faso.',
                'content': 'Le digital prend de plus en plus d\'importance au Burkina Faso. Avec l\'augmentation de l\'accès à Internet, avoir un site web devient indispensable pour votre entreprise. Les consommateurs recherchent de plus en plus les produits et services en ligne, et votre absence du web peut signifier perdre des opportunités commerciales importantes.',
                'category': categories[0] if categories else None,
                'tags': tags[:3],
                'published': True,
                'published_at': timezone.now() - timedelta(days=5),
                'meta_title': 'Pourquoi avoir un site web en 2026 au Burkina Faso ?',
                'meta_description': 'Découvrez pourquoi il est essentiel pour votre entreprise d\'avoir une présence en ligne au Burkina Faso en 2026.'
            },
            {
                'title': 'Les 5 erreurs SEO à éviter pour votre site web',
                'excerpt': 'Évitez ces erreurs courantes qui nuisent au référencement de votre site web.',
                'content': 'Le SEO est crucial pour la visibilité de votre site. Voici les 5 erreurs les plus courantes à éviter : 1) Ignorer la vitesse de chargement, 2) Négliger le mobile, 3) Oublier les balises meta, 4) Dupliquer le contenu, 5) Ignorer les backlinks. Apprenez comment les corriger pour améliorer votre référencement.',
                'category': categories[1] if len(categories) > 1 else None,
                'tags': tags[2:5],
                'published': True,
                'published_at': timezone.now() - timedelta(days=10),
                'meta_title': 'Les 5 erreurs SEO à éviter - SiraWeb',
                'meta_description': 'Découvrez les erreurs SEO les plus courantes et comment les éviter pour améliorer votre référencement.'
            },
            {
                'title': 'Comment créer un site e-commerce performant au Burkina Faso',
                'excerpt': 'Guide complet pour lancer votre boutique en ligne au Burkina Faso avec succès.',
                'content': 'Créer un site e-commerce au Burkina Faso nécessite une approche adaptée au marché local. Il faut considérer les moyens de paiement disponibles, la logistique de livraison, et les habitudes des consommateurs burkinabè. Nous vous guidons à travers les étapes essentielles.',
                'category': categories[0] if categories else None,
                'tags': tags[4:7] if len(tags) > 6 else tags[:3],
                'published': True,
                'published_at': timezone.now() - timedelta(days=15),
                'meta_title': 'Créer un site e-commerce au Burkina Faso - Guide',
                'meta_description': 'Guide complet pour créer et lancer votre boutique en ligne au Burkina Faso avec succès.'
            },
            {
                'title': 'Tendances design web 2026 : ce qui va marquer',
                'excerpt': 'Découvrez les tendances design qui vont dominer le web en 2026.',
                'content': 'Le design web évolue constamment. En 2026, nous observons plusieurs tendances majeures : les interfaces minimalistes avec beaucoup d\'espace blanc, les animations subtiles et performantes, les couleurs audacieuses, et l\'accent sur l\'accessibilité. Ces tendances façonnent l\'expérience utilisateur moderne.',
                'category': categories[2] if len(categories) > 2 else None,
                'tags': tags[5:8] if len(tags) > 7 else tags[:3],
                'published': True,
                'published_at': timezone.now() - timedelta(days=20),
                'meta_title': 'Tendances design web 2026 - SiraWeb',
                'meta_description': 'Découvrez les tendances design qui vont marquer le web en 2026 et comment les intégrer à votre site.'
            },
            {
                'title': 'Marketing digital au Burkina Faso : stratégies efficaces',
                'excerpt': 'Découvrez les meilleures stratégies de marketing digital adaptées au marché burkinabè.',
                'content': 'Le marketing digital au Burkina Faso présente des opportunités uniques. Avec la croissance de l\'utilisation des smartphones et des réseaux sociaux, les entreprises peuvent atteindre leur audience de manière plus ciblée. Nous explorons les stratégies les plus efficaces pour votre entreprise.',
                'category': categories[3] if len(categories) > 3 else None,
                'tags': tags[3:6] if len(tags) > 5 else tags[:3],
                'published': True,
                'published_at': timezone.now() - timedelta(days=25),
                'meta_title': 'Marketing digital Burkina Faso - Stratégies efficaces',
                'meta_description': 'Découvrez les meilleures stratégies de marketing digital adaptées au marché burkinabè pour développer votre entreprise.'
            },
            {
                'title': 'Optimiser la vitesse de votre site web : guide pratique',
                'excerpt': 'Conseils pratiques pour améliorer les performances et la vitesse de chargement de votre site.',
                'content': 'La vitesse de chargement est cruciale pour l\'expérience utilisateur et le SEO. Un site lent peut faire perdre jusqu\'à 50% de vos visiteurs. Nous vous donnons des conseils pratiques pour optimiser les images, minimiser le CSS/JS, utiliser la mise en cache, et choisir un bon hébergement.',
                'category': categories[0] if categories else None,
                'tags': tags[6:8] if len(tags) > 7 else tags[:3],
                'published': True,
                'published_at': timezone.now() - timedelta(days=30),
                'meta_title': 'Optimiser vitesse site web - Guide pratique',
                'meta_description': 'Conseils pratiques pour améliorer les performances et la vitesse de chargement de votre site web.'
            },
        ]

        for data in articles_data:
            tags_list = data.pop('tags', [])
            article, created = Article.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                article.tags.set(tags_list)
                self.stdout.write(f'  ✓ Article créé: {article.title}')

    def create_team(self):
        """Crée des membres de l'équipe."""
        team_data = [
            {
                'name': 'Jean Kaboré',
                'role': 'Directeur Technique',
                'bio': 'Expert en développement web avec 10 ans d\'expérience.',
                'order': 1
            },
            {
                'name': 'Aminata Traoré',
                'role': 'Designer UI/UX',
                'bio': 'Spécialiste en design d\'interfaces modernes et intuitives.',
                'order': 2
            },
        ]

        for data in team_data:
            member, created = TeamMember.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  ✓ Membre créé: {member.name}')

    def create_testimonials(self):
        """Crée des témoignages clients."""
        testimonials_data = [
            {
                'client_name': 'Ousmane Sawadogo',
                'client_company': 'Entreprise XYZ',
                'client_role': 'Directeur Général',
                'content': 'SiraWeb a créé un site web exceptionnel pour notre entreprise. Le résultat dépasse nos attentes !',
                'rating': 5,
                'order': 1
            },
            {
                'client_name': 'Fatou Diallo',
                'client_company': 'Boutique Moda',
                'client_role': 'Propriétaire',
                'content': 'Notre site e-commerce fonctionne parfaitement. Les ventes en ligne ont augmenté de 40% depuis le lancement.',
                'rating': 5,
                'order': 2
            },
        ]

        for data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                client_name=data['client_name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  ✓ Témoignage créé: {testimonial.client_name}')

    def create_partners(self):
        """Crée des partenaires."""
        partners_data = [
            {'name': 'Partenaire 1', 'order': 1},
            {'name': 'Partenaire 2', 'order': 2},
        ]

        for data in partners_data:
            partner, created = Partner.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  ✓ Partenaire créé: {partner.name}')
