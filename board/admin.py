from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from .models import Profile, Category, Ad, Comment


class CustomAdminSite(admin.AdminSite):
    """Кастомний Admin Site"""
    site_header = "Адмін-панель Дошки оголошень"
    site_title = "Дошка оголошень"
    index_title = "Ласкаво просимо до адміністративної панелі"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('statistics/', self.admin_view(self.statistics_view), name="statistics"),
        ]
        return custom_urls + urls

    def statistics_view(self, request):
        """Додає сторінку статистики в адмінку"""
        last_month = timezone.now() - timedelta(days=30)
        ads_last_month = Ad.objects.filter(created_at__gte=last_month).count()
        active_ads = Ad.objects.filter(is_active=True).count()
        inactive_ads = Ad.objects.filter(is_active=False).count()
        comments_count = Comment.objects.count()
        category_stats = Category.objects.annotate(num_ads=Count('ad')).values('name', 'num_ads')

        context = {
            'ads_last_month': ads_last_month,
            'active_ads': active_ads,
            'inactive_ads': inactive_ads,
            'category_stats': category_stats,
            'comments_count': comments_count,
        }

        return render(request, 'admin/statistics.html', context)

    def index(self, request, extra_context=None):
        """Додаємо кастомне посилання на статистику в головну сторінку адмінки"""
        extra_context = extra_context or {}
        extra_context['custom_statistics_link'] = '/admin/statistics/'
        return super().index(request, extra_context)




# Використовуємо кастомний Admin Site
admin_site = CustomAdminSite(name='custom_admin')


# Реєструємо моделі через кастомний `admin_site`
@admin.register(Profile, site=admin_site)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'email', 'is_active', 'is_staff')
    search_fields = ('user', 'email', 'phone_number')


@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'get_active_ads_count')
    search_fields = ('name', 'description')


@admin.register(Ad, site=admin_site)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'updated_at', 'is_active', 'user', 'category', 'view_statistics')
    list_filter = ('is_active', 'category', 'user')
    search_fields = ('title', 'description', 'price')
    date_hierarchy = 'created_at'

    def view_statistics(self, obj):
        """Додає кнопку для перегляду статистики"""
        return format_html('<a href="/admin/statistics/" class="button">📊 Переглянути статистику</a>')

    view_statistics.short_description = "Статистика"


@admin.register(Comment, site=admin_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'ad', 'created_at')
    search_fields = ('content', 'user__username', 'ad__title')
    list_filter = ('ad', 'user')

admin_site = CustomAdminSite(name='custom_admin')

# Реєструємо моделі в кастомному admin_site
admin_site.register(Profile, ProfileAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Ad, AdAdmin)
admin_site.register(Comment, CommentAdmin)

