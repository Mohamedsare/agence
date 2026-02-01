from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class Category(models.Model):
    """Catégorie pour les articles de blog."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Tag pour les articles de blog."""
    name = models.CharField(max_length=50, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    """Article de blog."""
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=300, verbose_name="Extrait")
    content = models.TextField(verbose_name="Contenu")
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name="Image mise en avant")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Catégorie")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")
    author = models.CharField(max_length=100, default="SiraWeb", verbose_name="Auteur")
    published = models.BooleanField(default=False, verbose_name="Publié")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de publication")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(max_length=65, blank=True, verbose_name="Meta titre (SEO)")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta description (SEO)")

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})


class ContactMessage(models.Model):
    """Message de contact."""
    name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    company = models.CharField(max_length=100, blank=True, verbose_name="Entreprise")
    budget = models.CharField(max_length=50, blank=True, verbose_name="Budget")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False, verbose_name="Lu")

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"


class Service(models.Model):
    """Service proposé par l'agence."""
    SERVICE_CHOICES = [
        ('vitrine', 'Création de site vitrine'),
        ('ecommerce', 'Site e-commerce'),
        ('institutionnel', 'Site institutionnel'),
        ('landing', 'Landing pages'),
        ('refonte', 'Refonte UI/UX'),
        ('seo', 'SEO naturel'),
        ('sea', 'SEA (Google Ads)'),
        ('maintenance', 'Maintenance & hébergement'),
    ]
    
    name = models.CharField(max_length=100, choices=SERVICE_CHOICES, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    short_description = models.TextField(max_length=200, verbose_name="Description courte")
    full_description = models.TextField(verbose_name="Description complète")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icône")
    featured_image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Image")
    meta_title = models.CharField(max_length=65, blank=True, verbose_name="Meta titre (SEO)")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Meta description (SEO)")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['order', 'name']

    def __str__(self):
        return self.get_name_display()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_name_display())
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})


class TeamMember(models.Model):
    """Membre de l'équipe."""
    name = models.CharField(max_length=100, verbose_name="Nom")
    role = models.CharField(max_length=100, verbose_name="Rôle")
    bio = models.TextField(blank=True, verbose_name="Biographie")
    photo = models.ImageField(upload_to='team/', blank=True, null=True, verbose_name="Photo")
    email = models.EmailField(blank=True, verbose_name="Email")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.role}"


class Testimonial(models.Model):
    """Témoignage client."""
    client_name = models.CharField(max_length=100, verbose_name="Nom du client")
    client_company = models.CharField(max_length=100, blank=True, verbose_name="Entreprise")
    client_role = models.CharField(max_length=100, blank=True, verbose_name="Rôle")
    content = models.TextField(verbose_name="Témoignage")
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name="Photo")
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)], verbose_name="Note")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.client_company}"


class Partner(models.Model):
    """Partenaire."""
    name = models.CharField(max_length=100, verbose_name="Nom")
    logo = models.ImageField(upload_to='partners/', verbose_name="Logo")
    website = models.URLField(blank=True, verbose_name="Site web")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    active = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    """Projet portfolio/réalisation."""
    name = models.CharField(max_length=100, verbose_name="Nom du projet")
    company = models.CharField(max_length=100, blank=True, verbose_name="Entreprise/Client")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='portfolio/', verbose_name="Image du projet")
    website_url = models.URLField(blank=True, verbose_name="URL du site web")
    detail_url = models.URLField(blank=True, verbose_name="URL de détail (optionnel)")
    category = models.CharField(
        max_length=50,
        choices=[
            ('vitrine', 'Site vitrine'),
            ('ecommerce', 'E-commerce'),
            ('institutionnel', 'Institutionnel'),
            ('landing', 'Landing page'),
            ('refonte', 'Refonte'),
            ('autre', 'Autre'),
        ],
        default='vitrine',
        verbose_name="Catégorie"
    )
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Projet portfolio"
        verbose_name_plural = "Projets portfolio"
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.company or 'Sans entreprise'}"
