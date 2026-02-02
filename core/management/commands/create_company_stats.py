"""
Commande Django pour créer les statistiques de l'entreprise
Usage: python manage.py create_company_stats
"""
from django.core.management.base import BaseCommand
from core.models import CompanyStats


class Command(BaseCommand):
    help = 'Cree les statistiques de l\'entreprise avec les valeurs par defaut'

    def handle(self, *args, **options):
        stats, created = CompanyStats.objects.get_or_create(
            active=True,
            defaults={
                'projects_count': 50,
                'years_experience': 5,
                'client_satisfaction': 98,
                'active': True,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'[OK] Statistiques creees: {stats.projects_count} projets, {stats.years_experience} ans, {stats.client_satisfaction}%'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'[UPDATE] Statistiques existent deja: {stats.projects_count} projets, {stats.years_experience} ans, {stats.client_satisfaction}%'
                )
            )
