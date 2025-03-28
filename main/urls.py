from django.urls import path
from . import views
from .views import ServiceView, ContactView

app_name = 'main'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('services/', ServiceView.as_view(), name='services'),
]
