"""
URL configuration for my_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.main, name='main')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='main')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from board.admin import admin_site

urlpatterns = i18n_patterns(
    path('admin/', admin_site.urls),
    #path('admin/', admin.site.urls),
    path('home/', include('main.urls')),

    path('i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += [
    #path('', include('board.urls')),
    path('accounts/', include('allauth.urls')),
    path('board/', include('board.urls')),
]