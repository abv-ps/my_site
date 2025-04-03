"""
URL configuration for the 'board' application.

This module defines the URL patterns for the 'board' app, mapping URLs to the corresponding views.
It includes routes for user authentication, profile management, ad operations, and statistics.

Routes:
    - '/'                      -> List of advertisements (ad_list)
    - 'ad/<int:ad_id>/'        -> Advertisement details (ad_detail)
    - 'profile/<int:user_id>/' -> User profile page (user_profile)
    - 'profile/<int:user_id>/add_ad/' -> Add a new advertisement (add_ad)
    - 'profile/<int:user_id>/edit/' -> Edit user profile (edit_profile)
    - 'profile/<int:user_id>/change-password/' -> Change user password (change_password)
    - 'statistics/'            -> View advertisement statistics (ad_statistics)
    - 'logout/'                -> User logout (CustomLogoutView)
    - 'login/'                 -> User login (CustomLoginView)
    - 'register/'              -> User registration (register_view)
    - 'delete-account/<int:user_id>/' -> Delete user account (delete_account)

Constants:
    - APP_NAME (str): Application namespace identifier.

Imports:
    - Django's path function for URL pattern definitions.
    - Views from the 'board' app including both function-based and class-based views.
"""

from django.urls import path

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
    path('profile/<int:user_id>/add_ad/', views.add_ad, name='add_ad'),
    path('profile/<int:user_id>/edit/', edit_profile_view, name='edit_profile'),
    path('profile/<int:user_id>/change-password/', change_password_view, name='change_password'),
    path('statistics/', views.ad_statistics, name='ad_statistics'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path("delete-account/<int:user_id>/", delete_account_view, name="delete_account"),
]
