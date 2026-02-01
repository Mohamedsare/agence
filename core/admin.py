from django.contrib import admin
from .models import (
    Article, Category, Tag, ContactMessage, Service,
    TeamMember, Testimonial, Partner, Portfolio
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
