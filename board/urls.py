from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import CustomLoginView

app_name = "board"

urlpatterns = [

    path('', views.ad_list, name='ad_list'),
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('statistics/', views.ad_statistics, name='ad_statistics'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
