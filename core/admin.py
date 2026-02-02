from django.contrib import admin
from .models import (
    Article, Category, Tag, ContactMessage, Service,
    TeamMember, Testimonial, Partner, Portfolio, Technology, AnonymousCTA, WhatsAppConfig, FAQ, CompanyStats, PageView
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published', 'published_at', 'created_at']
    list_filter = ['published', 'category', 'tags', 'created_at']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'published_at'
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image', 'author')
        }),
        ('Classification', {
            'fields': ('category', 'tags', 'published', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'created_at', 'read']
    list_filter = ['read', 'created_at']
    search_fields = ['name', 'email', 'company', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['get_name_display', 'slug', 'order', 'active']
    list_filter = ['active', 'name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'order', 'active']
    list_filter = ['active']
    ordering = ['order', 'name']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_company', 'rating', 'order', 'active']
    list_filter = ['active', 'rating']
    ordering = ['order', '-created_at']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'order', 'active']
    list_filter = ['active']
    ordering = ['order', 'name']


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'category', 'order', 'active', 'created_at']
    list_filter = ['active', 'category', 'created_at']
    search_fields = ['name', 'company', 'description']
    ordering = ['order', '-created_at']
    fieldsets = (
        ('Informations principales', {
            'fields': ('name', 'company', 'description', 'category')
        }),
        ('Médias', {
            'fields': ('image',)
        }),
        ('Liens', {
            'fields': ('website_url', 'detail_url')
        }),
        ('Affichage', {
            'fields': ('order', 'active')
        }),
    )


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['name']
    ordering = ['order', 'name']
    fieldsets = (
        ('Informations principales', {
            'fields': ('name', 'logo')
        }),
        ('Affichage', {
            'fields': ('order', 'active')
        }),
    )


@admin.register(AnonymousCTA)
class AnonymousCTAAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'active', 'updated_at']
    list_filter = ['active', 'updated_at']
    fieldsets = (
        ('Image', {
            'fields': ('image',)
        }),
        ('Affichage', {
            'fields': ('active',)
        }),
    )
    
    def has_add_permission(self, request):
        # Permettre l'ajout seulement s'il n'y a pas encore d'instance
        return AnonymousCTA.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        # Empêcher la suppression pour garder au moins une instance
        return False


@admin.register(WhatsAppConfig)
class WhatsAppConfigAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'active', 'updated_at']
    list_filter = ['active', 'updated_at']
    fieldsets = (
        ('Configuration WhatsApp', {
            'fields': ('phone_number', 'message'),
            'description': 'Configurez le numéro WhatsApp et le message par défaut pour le bouton flottant.'
        }),
        ('Affichage', {
            'fields': ('active',)
        }),
    )
    
    def has_add_permission(self, request):
        # Permettre l'ajout seulement s'il n'y a pas encore d'instance
        return WhatsAppConfig.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        # Empêcher la suppression pour garder au moins une instance
        return False


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['question', 'answer']
    ordering = ['order', 'question']
    fieldsets = (
        ('Contenu', {
            'fields': ('question', 'answer')
        }),
        ('Affichage', {
            'fields': ('order', 'active')
        }),
    )


@admin.register(CompanyStats)
class CompanyStatsAdmin(admin.ModelAdmin):
    list_display = ['projects_count', 'years_experience', 'client_satisfaction', 'active', 'updated_at']
    list_filter = ['active', 'updated_at']
    fieldsets = (
        ('Statistiques', {
            'fields': ('projects_count', 'years_experience', 'client_satisfaction'),
            'description': 'Modifiez les statistiques affichées sur la page "À propos".'
        }),
        ('Affichage', {
            'fields': ('active',)
        }),
    )
    
    def has_add_permission(self, request):
        # Permettre l'ajout seulement s'il n'y a pas encore d'instance
        return CompanyStats.objects.count() == 0
    
    def has_delete_permission(self, request, obj=None):
        # Empêcher la suppression pour garder au moins une instance
        return False


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['path', 'ip_address', 'country', 'city', 'created_at', 'is_bot']
    list_filter = ['is_bot', 'country_code', 'created_at']
    search_fields = ['path', 'ip_address', 'country', 'city']
    readonly_fields = ['path', 'ip_address', 'country', 'country_code', 'city', 'user_agent', 'referer', 'is_bot', 'created_at']
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        # Empêcher l'ajout manuel, les visites sont trackées automatiquement
        return False
    
    def has_change_permission(self, request, obj=None):
        # Les visites sont en lecture seule
        return False
