import os

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from my_site.settings import BASE_DIR
from . import views
from .views import (CustomLoginView,
        CustomLogoutView,
        register_view,
        edit_profile_view,
        change_password_view,
        user_profile,
        delete_account_view
)

app_name = "board"

urlpatterns = [

    path('', views.ad_list, name='ad_list'),
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('profile/<int:user_id>/', user_profile, name='user_profile'),
    path('profile/<int:user_id>/edit/', edit_profile_view, name='edit_profile'),
    path('profile/<int:user_id>/change-password/', change_password_view, name='change_password'),
    path('statistics/', views.ad_statistics, name='ad_statistics'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path("delete-account/<int:user_id>/", delete_account_view, name="delete_account"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
