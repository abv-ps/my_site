from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from .models import Ad, User, Category, Comment, Profile
from .forms import CommentForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш акаунт успішно створено!')
            return redirect('board:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def ad_list(request):
    ads = Ad.objects.filter(is_active=True)
    return render(request, 'board/ad_list.html', {'ads': ads})


def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    comments = ad.comments.all()
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.ad = ad
        comment.user = request.user
        comment.save()
    return render(request, 'board/ad_detail.html', {'ad': ad, 'comments': comments, 'form': form})


@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'board/profile.html', {'user': user, 'profile': profile})

class CustomLoginView(LoginView):
    def get_success_url(self):
        print(f"Redirecting to profile for user {self.request.user.username}")
        return f'/board/profile/{self.request.user.username}/'

def ad_statistics(request):
    last_month = timezone.now() - timedelta(days=30)
    ads_last_month = Ad.objects.filter(created_at__gte=last_month).count()
    active_ads = Ad.objects.filter(is_active=True).count()
    inactive_ads = Ad.objects.filter(is_active=False).count()
    comments_count = Comment.objects.count()
    category_stats = Category.objects.annotate(num_ads=Count('ad')).values('name', 'num_ads')

    return render(request, 'board/statistics.html', {
        'ads_last_month': ads_last_month,
        'active_ads': active_ads,
        'inactive_ads': inactive_ads,
        'category_stats': category_stats,
        'comments_count': comments_count
    })
