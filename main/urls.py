from django.urls import path, re_path
from . import views
from .views import ServiceView, ContactView

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('services/', ServiceView.as_view(), name='services'),
]
