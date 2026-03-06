"""
Commande Django pour créer des articles de blog par défaut
Usage: python manage.py create_blog_articles
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Article, Category, Tag


class Command(BaseCommand):
    help = 'Crée des articles de blog par défaut pour FASOWEB'

    def handle(self, *args, **options):
        # Créer les catégories par défaut
        categories_data = [
            {
                'name': 'Développement Web',
                'slug': 'developpement-web',
                'description': 'Articles sur le développement web, les technologies et les bonnes pratiques.',
            },
            {
                'name': 'SEO & Référencement',
                'slug': 'seo-referencement',
                'description': 'Conseils et astuces pour améliorer votre référencement naturel.',
            },
            {
                'name': 'Conseils & Astuces',
                'slug': 'conseils-astuces',
                'description': 'Conseils pratiques pour améliorer votre présence en ligne.',
            },
            {
                'name': 'Actualités',
                'slug': 'actualites',
                'description': 'Actualités et nouveautés de FASOWEB et du web au Burkina Faso.',
            },
        ]
        
        categories_map = {}
        for cat_data in categories_data:
            category, created = Category.objects.update_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                }
            )
            categories_map[cat_data['slug']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Categorie creee: {category.name}'))
        
        # Créer les tags par défaut
        tags_data = [
            'Django', 'Python', 'SEO', 'Web Design', 'E-commerce', 
            'Responsive', 'Performance', 'Sécurité', 'Burkina Faso', 'Afrique'
        ]
        
        tags_map = {}
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags_map[tag_name] = tag
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Tag cree: {tag.name}'))
        
        # Créer les articles par défaut
        articles_data = [
            {
                'title': 'Pourquoi avoir un site web est essentiel pour votre entreprise au Burkina Faso',
                'slug': 'pourquoi-avoir-un-site-web-essentiel-burkina-faso',
                'excerpt': 'Découvrez pourquoi un site web est devenu indispensable pour les entreprises au Burkina Faso en 2024.',
                'content': '''<h2>Introduction</h2>
<p>Dans un monde de plus en plus connecté, avoir une présence en ligne n'est plus une option mais une nécessité. Au Burkina Faso, de plus en plus d'entreprises réalisent l'importance d'avoir un site web professionnel.</p>

<h2>Les avantages d'un site web</h2>
<ul>
<li><strong>Visibilité 24/7</strong> : Votre site est accessible à tout moment, même quand votre bureau est fermé.</li>
<li><strong>Crédibilité</strong> : Un site web professionnel renforce la confiance de vos clients.</li>
<li><strong>Portée géographique</strong> : Atteignez des clients au-delà de votre zone géographique immédiate.</li>
<li><strong>Marketing rentable</strong> : Un site web est un investissement unique qui continue de travailler pour vous.</li>
</ul>

<h2>Conclusion</h2>
<p>Investir dans un site web est l'une des meilleures décisions que vous puissiez prendre pour votre entreprise. Contactez FASOWEB pour discuter de votre projet.</p>''',
                'author': 'FASOWEB',
                'category': 'conseils-astuces',
                'tags': ['Burkina Faso', 'Conseils & Astuces'],
                'published': True,
                'meta_title': 'Pourquoi avoir un site web au Burkina Faso | FASOWEB',
                'meta_description': 'Découvrez pourquoi un site web est essentiel pour votre entreprise au Burkina Faso. Conseils et avantages expliqués.',
            },
            {
                'title': 'Les 5 erreurs à éviter lors de la création de votre site web',
                'slug': '5-erreurs-eviter-creation-site-web',
                'excerpt': 'Évitez ces erreurs courantes lors de la création de votre site web pour garantir le succès de votre projet.',
                'content': '''<h2>Introduction</h2>
<p>Créer un site web peut sembler simple, mais de nombreuses erreurs peuvent compromettre votre projet. Voici les 5 erreurs les plus courantes à éviter.</p>

<h2>1. Ne pas penser mobile-first</h2>
<p>Avec plus de 60% des internautes utilisant leur smartphone, votre site doit être parfaitement adapté aux mobiles.</p>

<h2>2. Ignorer le SEO</h2>
<p>Un site web invisible sur Google ne sert à rien. Pensez au référencement dès le début.</p>

<h2>3. Contenu de mauvaise qualité</h2>
<p>Le contenu est roi. Investissez dans un contenu de qualité qui apporte de la valeur à vos visiteurs.</p>

<h2>4. Temps de chargement trop long</h2>
<p>Les utilisateurs quittent un site qui met plus de 3 secondes à charger. Optimisez les performances.</p>

<h2>5. Ne pas prévoir la maintenance</h2>
<p>Un site web nécessite des mises à jour régulières. Prévoyez un budget pour la maintenance.</p>

<h2>Conclusion</h2>
<p>Évitez ces erreurs et votre site web sera un véritable atout pour votre entreprise.</p>''',
                'author': 'FASOWEB',
                'category': 'conseils-astuces',
                'tags': ['Web Design', 'Conseils & Astuces', 'Performance'],
                'published': True,
                'meta_title': '5 erreurs à éviter pour votre site web | FASOWEB',
                'meta_description': 'Découvrez les 5 erreurs les plus courantes à éviter lors de la création de votre site web. Conseils d\'experts.',
            },
            {
                'title': 'Comment améliorer votre référencement naturel (SEO) au Burkina Faso',
                'slug': 'ameliorer-referencement-seo-burkina-faso',
                'excerpt': 'Guide complet pour améliorer votre référencement naturel et apparaître en première page de Google au Burkina Faso.',
                'content': '''<h2>Introduction</h2>
<p>Le référencement naturel (SEO) est crucial pour que votre site web soit visible sur Google. Voici comment l'améliorer.</p>

<h2>1. Optimiser vos mots-clés</h2>
<p>Recherchez les mots-clés pertinents pour votre activité au Burkina Faso. Utilisez des outils comme Google Keyword Planner.</p>

<h2>2. Créer du contenu de qualité</h2>
<p>Google privilégie les sites avec du contenu original, utile et régulièrement mis à jour.</p>

<h2>3. Optimiser les balises meta</h2>
<p>Assurez-vous que chaque page a un titre et une description optimisés pour le SEO.</p>

<h2>4. Améliorer la vitesse de chargement</h2>
<p>Un site rapide est mieux classé par Google. Optimisez vos images et votre code.</p>

<h2>5. Obtenir des backlinks</h2>
<p>Les liens depuis d'autres sites vers le vôtre améliorent votre autorité. Participez à des partenariats locaux.</p>

<h2>Conclusion</h2>
<p>Le SEO est un travail de longue haleine, mais les résultats en valent la peine. Contactez FASOWEB pour un audit SEO.</p>''',
                'author': 'FASOWEB',
                'category': 'seo-referencement',
                'tags': ['SEO', 'Burkina Faso', 'Conseils & Astuces'],
                'published': True,
                'meta_title': 'Améliorer votre SEO au Burkina Faso | FASOWEB',
                'meta_description': 'Guide complet pour améliorer votre référencement naturel au Burkina Faso. Conseils SEO pratiques et efficaces.',
            },
            {
                'title': 'Django vs WordPress : Quel CMS choisir pour votre site web ?',
                'slug': 'django-vs-wordpress-quel-cms-choisir',
                'excerpt': 'Comparaison entre Django et WordPress pour vous aider à choisir la meilleure solution pour votre site web.',
                'content': '''<h2>Introduction</h2>
<p>Choisir entre Django et WordPress peut être difficile. Voici une comparaison pour vous aider à décider.</p>

<h2>WordPress</h2>
<h3>Avantages :</h3>
<ul>
<li>Facile à utiliser, même pour les débutants</li>
<li>Grande communauté et nombreux plugins</li>
<li>Idéal pour les blogs et sites vitrines simples</li>
</ul>

<h3>Inconvénients :</h3>
<ul>
<li>Moins flexible pour les projets complexes</li>
<li>Peut être lent si mal optimisé</li>
<li>Sécurité à surveiller avec les plugins</li>
</ul>

<h2>Django</h2>
<h3>Avantages :</h3>
<ul>
<li>Très flexible et personnalisable</li>
<li>Performance optimale</li>
<li>Sécurité renforcée</li>
<li>Idéal pour les applications web complexes</li>
</ul>

<h3>Inconvénients :</h3>
<ul>
<li>Nécessite des compétences en programmation</li>
<li>Développement plus long</li>
<li>Coût plus élevé</li>
</ul>

<h2>Quand choisir quoi ?</h2>
<p><strong>WordPress</strong> : Blog, site vitrine simple, e-commerce basique</p>
<p><strong>Django</strong> : Application web complexe, site sur mesure, besoins spécifiques</p>

<h2>Conclusion</h2>
<p>Le choix dépend de vos besoins. FASOWEB peut vous aider à choisir la meilleure solution pour votre projet.</p>''',
                'author': 'FASOWEB',
                'category': 'developpement-web',
                'tags': ['Django', 'Python', 'Web Design'],
                'published': True,
                'meta_title': 'Django vs WordPress : Quel CMS choisir ? | FASOWEB',
                'meta_description': 'Comparaison détaillée entre Django et WordPress. Découvrez quel CMS choisir pour votre site web selon vos besoins.',
            },
            {
                'title': 'FASOWEB lance son nouveau site web : Découvrez nos services',
                'slug': 'fasoweb-lance-nouveau-site-web',
                'excerpt': 'FASOWEB est fier de présenter son nouveau site web avec des fonctionnalités améliorées et un design moderne.',
                'content': '''<h2>Introduction</h2>
<p>Nous sommes ravis de vous présenter le nouveau site web de FASOWEB, entièrement repensé pour mieux vous servir.</p>

<h2>Nouvelles fonctionnalités</h2>
<ul>
<li><strong>Design moderne</strong> : Interface épurée et professionnelle</li>
<li><strong>Performance optimisée</strong> : Chargement ultra-rapide</li>
<li><strong>Mobile-first</strong> : Parfaitement adapté aux smartphones</li>
<li><strong>SEO amélioré</strong> : Meilleure visibilité sur Google</li>
</ul>

<h2>Nos services</h2>
<p>Découvrez notre gamme complète de services :</p>
<ul>
<li>Création de sites web sur mesure</li>
<li>Référencement naturel (SEO)</li>
<li>E-commerce</li>
<li>Maintenance et hébergement</li>
</ul>

<h2>Contactez-nous</h2>
<p>Besoin d'un site web professionnel ? Contactez FASOWEB dès aujourd'hui pour un devis gratuit.</p>''',
                'author': 'FASOWEB',
                'category': 'actualites',
                'tags': ['FASOWEB', 'Burkina Faso', 'Actualités'],
                'published': True,
                'meta_title': 'FASOWEB lance son nouveau site web | Actualités',
                'meta_description': 'Découvrez le nouveau site web de FASOWEB avec des fonctionnalités améliorées et un design moderne.',
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for article_data in articles_data:
            # Récupérer la catégorie
            category = categories_map.get(article_data.get('category'))
            
            # Récupérer les tags
            tags = []
            for tag_name in article_data.get('tags', []):
                if tag_name in tags_map:
                    tags.append(tags_map[tag_name])
            
            # Créer ou mettre à jour l'article
            article, created = Article.objects.update_or_create(
                slug=article_data['slug'],
                defaults={
                    'title': article_data['title'],
                    'excerpt': article_data.get('excerpt', ''),
                    'content': article_data.get('content', ''),
                    'author': article_data.get('author', 'FASOWEB'),
                    'category': category,
                    'published': article_data.get('published', False),
                    'published_at': timezone.now() if article_data.get('published') else None,
                    'meta_title': article_data.get('meta_title', ''),
                    'meta_description': article_data.get('meta_description', ''),
                }
            )
            
            # Ajouter les tags
            if tags:
                article.tags.set(tags)
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'[OK] Article cree: {article.title}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'[UPDATE] Article mis a jour: {article.title}'))
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n[SUCCESS] Termine ! {created_count} article(s) cree(s), {updated_count} article(s) mis a jour.'
            )
        )
