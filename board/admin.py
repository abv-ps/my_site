"""
This module contains the configuration for the custom Django Admin Site,
along with the registration of several models, including Profile, Category,
Ad, and Comment.

It extends the `admin.AdminSite` class to provide custom functionality for
the advertisement board's administration panel, including a custom statistics
page and custom links on the admin index page.

The module includes:

- A custom `CustomAdminSite` class to extend Django's admin panel with custom URLs
  and views.
- Admin configurations for the `Profile`, `Category`, `Ad`, and `Comment` models.
- Custom views for displaying statistics about ads, comments, and categories.
- Custom list displays, search fields, and filter options for managing the models.

Module Dependencies:
- `django.contrib.admin`: For admin site customizations.
- `django.urls`: For defining URL paths for custom views.
- `django.shortcuts.render`: For rendering HTML templates.
- `django.utils.html.format_html`: For safely formatting HTML in Django templates.
- `django.utils.timezone`: For timezone-related operations.
- `django.db.models.Count`: For counting related objects.
- `datetime.timedelta`: For handling date intervals.
- `.models`: For importing the `Profile`, `Category`, `Ad`, and `Comment` models.

"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from .models import Profile, Category, Ad, Comment


class CustomAdminSite(admin.AdminSite):
    """
    Custom Admin Site for the advertisement board.

    Attributes:
        site_header (str): The header for the admin panel.
        site_title (str): The title of the admin panel.
        index_title (str): The title of the admin index page.

    Methods:
        get_urls:
            Args:
                self (CustomAdminSite): The instance of the CustomAdminSite class.

            Returns:
                list: List of custom and default URLs.

        statistics_view:
            Args:
                self (CustomAdminSite): The instance of the CustomAdminSite class.
                request (HttpRequest): The HTTP request object.

            Returns:
                HttpResponse: The rendered statistics page with context data.

        index:
            Args:
                self (CustomAdminSite): The instance of the CustomAdminSite class.
                request (HttpRequest): The HTTP request object.
                extra_context (dict, optional): Extra context to pass to the template.

            Returns:
                HttpResponse: The rendered admin index page with additional context.
    """
    site_header = "Адмін-панель Дошки оголошень"
    site_title = "Дошка оголошень"
    index_title = "Ласкаво просимо до адміністративної панелі"

    def get_urls(self):
        """
        Overrides the default URLs to add a custom statistics page.

        Args:
            self (CustomAdminSite): The instance of the CustomAdminSite class.

        Returns:
            list: List of custom URLs, including the statistics page.
        """
        urls = super().get_urls()
        custom_urls = [
            path('statistics/', self.admin_view(self.statistics_view), name="statistics"),
        ]
        return custom_urls + urls

    def statistics_view(self, request):
        """
        Displays statistics about ads, comments, and categories.

        Args:
            self (CustomAdminSite): The instance of the CustomAdminSite class.
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered statistics page with context data.
        """
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
        """
        Adds a custom link to the statistics page on the admin dashboard.

        Args:
            self (CustomAdminSite): The instance of the CustomAdminSite class.
            request (HttpRequest): The HTTP request object.
            extra_context (dict, optional): Extra context to pass to the template.

        Returns:
            HttpResponse: The rendered admin index page with the additional custom link.
        """
        extra_context = extra_context or {}
        extra_context['custom_statistics_link'] = '/admin/statistics/'
        return super().index(request, extra_context)


admin_site = CustomAdminSite(name='custom_admin')


@admin.register(Profile, site=admin_site)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Profile model.

    Attributes:
        list_display (tuple): The fields to display in the list view.
        search_fields (tuple): The fields to enable searching for.

    Methods:
        None
    """

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['email'].required = False
        return form
    list_display = ('user', 'bio', 'birth_date', 'phone_number', 'location', 'email', 'is_active', 'is_staff')
    search_fields = ('user', 'email', 'phone_number', 'bio', 'location')


@admin.register(Category, site=admin_site)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.

    Attributes:
        list_display (tuple): The fields to display in the list view.
        search_fields (tuple): The fields to enable searching for.

    Methods:
        None
    """
    list_display = ('name', 'description', 'get_active_ads_count')
    search_fields = ('name', 'description')


@admin.register(Ad, site=admin_site)
class AdAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Ad model.

    Attributes:
        list_display (tuple): The fields to display in the list view.
        list_filter (tuple): The fields to filter by.
        search_fields (tuple): The fields to enable searching for.
        date_hierarchy (str): The field to enable date-based navigation.

    Methods:
        view_statistics:
            Args:
                self (AdAdmin): The instance of the AdAdmin class.
                obj (Ad): The ad instance.

            Returns:
                str: HTML for the statistics button.
    """
    list_display = ('title', 'price', 'created_at', 'updated_at', 'is_active', 'user', 'category', 'view_statistics')
    list_filter = ('is_active', 'category', 'user')
    search_fields = ('title', 'description', 'price')
    date_hierarchy = 'created_at'

    def view_statistics(self, obj):
        """
        Adds a button to view statistics.

        Args:
            self (AdAdmin): The instance of the AdAdmin class.
            obj (Ad): The ad instance.

        Returns:
            str: HTML for the statistics button.
        """
        return format_html('<a href="/admin/statistics/" class="button">📊 Переглянути статистику</a>')

    view_statistics.short_description = "Статистика"


@admin.register(Comment, site=admin_site)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Comment model.

    Attributes:
        list_display (tuple): The fields to display in the list view.
        search_fields (tuple): The fields to enable searching for.
        list_filter (tuple): The fields to filter by.

    Methods:
        None
    """
    list_display = ('user', 'content', 'ad', 'created_at')
    search_fields = ('content', 'user__username', 'ad__title')
    list_filter = ('ad', 'user')


admin_site = CustomAdminSite(name='custom_admin')

# Register models with custom admin site
admin_site.register(Profile, ProfileAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Ad, AdAdmin)
admin_site.register(Comment, CommentAdmin)
