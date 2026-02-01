from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, Category, Service, ContactMessage


class CoreViewsTestCase(TestCase):
    """Tests basiques pour les vues principales."""
    
    def setUp(self):
        """Configuration initiale pour les tests."""
        self.client = Client()
        
    def test_home_page(self):
        """Test que la page d'accueil se charge correctement."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
    
    def test_services_list_page(self):
        """Test que la page liste des services se charge."""
        response = self.client.get(reverse('services_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/services_list.html')
    
    def test_about_page(self):
        """Test que la page À propos se charge."""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')
    
    def test_team_page(self):
        """Test que la page Équipe se charge."""
        response = self.client.get(reverse('team'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/team.html')
    
    def test_contact_page_get(self):
        """Test que la page contact se charge en GET."""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')
    
    def test_contact_form_submission(self):
        """Test la soumission du formulaire de contact."""
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+226 70 00 00 00',
            'company': 'Test Company',
            'budget': '500 000 - 1 000 000 FCFA',
            'message': 'Test message'
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(ContactMessage.objects.filter(email='test@example.com').exists())
    
    def test_blog_list_page(self):
        """Test que la page liste du blog se charge."""
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/blog_list.html')
    
    def test_robots_txt(self):
        """Test que robots.txt est accessible."""
        response = self.client.get(reverse('robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('User-agent', response.content.decode())
        self.assertIn('Sitemap', response.content.decode())


class CoreModelsTestCase(TestCase):
    """Tests pour les modèles."""
    
    def test_service_creation(self):
        """Test la création d'un service."""
        service = Service.objects.create(
            name='vitrine',
            short_description='Test service',
            full_description='Full description',
            order=1,
            active=True
        )
        self.assertEqual(str(service), 'Création de site vitrine')
        self.assertTrue(service.slug)
    
    def test_article_creation(self):
        """Test la création d'un article."""
        category = Category.objects.create(name='Test Category')
        article = Article.objects.create(
            title='Test Article',
            excerpt='Test excerpt',
            content='Test content',
            category=category,
            published=True
        )
        self.assertEqual(str(article), 'Test Article')
        self.assertTrue(article.slug)
        self.assertIsNotNone(article.published_at)
    
    def test_contact_message_creation(self):
        """Test la création d'un message de contact."""
        message = ContactMessage.objects.create(
            name='Test User',
            email='test@example.com',
            message='Test message'
        )
        self.assertEqual(str(message), 'Test User - test@example.com')
