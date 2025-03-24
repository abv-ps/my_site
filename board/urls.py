from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (CustomLoginView,
        register_view,
        edit_profile,
        change_password_view,
        user_profile
)

app_name = "board"

urlpatterns = [

    path('', views.ad_list, name='ad_list'),
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('profile/<str:username>/edit/', edit_profile, name='profile_edit'),
    path('profile/<str:username>/change-password/', change_password_view, name='change_password'),
    path('statistics/', views.ad_statistics, name='ad_statistics'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register_view, name='register'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("delete-account/", delete_account_view, name="delete_account"),
]
