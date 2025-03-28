"""
This module contains views for handling user authentication, advertisements, comments, profiles,
and statistics within the 'board' application of a Django project.

Functions:
- `register`: Handles user registration by displaying the registration form and saving the user.
- `ad_list`: Displays a list of active advertisements.
- `ad_detail`: Displays details for a specific advertisement and allows users to add comments.
- `user_profile`: Displays the profile page for a given user.
- `ad_statistics`: Displays statistics about advertisements, such as the number of ads created in the last month,
  the number of active/inactive ads, the number of comments, and the number of ads per category.

Classes:
- `CustomLoginView`: A custom login view that redirects the user to their profile page after successful login.

This module makes use of Django's built-in authentication views and form handling and integrates
models and forms from the `board` application, such as `Ad`, `Comment`, `Profile`, and `User`.
"""
from django.http import HttpResponse, HttpRequest, request, Http404
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from my_site import settings
from my_site.settings import MEDIA_ROOT, MEDIA_URL
from .models import Ad, User, Category, Comment, Profile
from .forms import CommentForm, RegistrationForm, UserProfileForm, PasswordChangeForm


def register_view(request) -> render:
    """
    Handles user registration.

    Displays the registration form and creates a new user upon form submission.
    Redirects the user to the login page upon successful registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered registration page or a redirect to the login page if the form is valid.
    """
    if request.user.is_authenticated:
        return redirect('board:user_profile', user_id=request.user.id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Ваш акаунт успішно створено!')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('board:user_profile', user_id=user.id)
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def ad_list(request) -> render:
    """
    Displays the list of active advertisements.

    Fetches all active advertisements and renders them in the ad list page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered ad list page with the active ads.
    """
    ads = Ad.objects.filter(is_active=True)
    return render(request, 'board/ad_list.html', {'ads': ads})


def ad_detail(request, ad_id: int) -> render:
    """
    Displays the details of a specific advertisement and handles comment submission.

    Fetches the advertisement by its ID, displays its details, and allows users to add comments.

    Args:
        request (HttpRequest): The HTTP request object.
        ad_id (int): The ID of the advertisement to display.

    Returns:
        HttpResponse: The rendered ad detail page with the ad's information and comments.
    """
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
def user_profile(request, user_id: int) -> render:
    """
    Відображає профіль користувача.

    Отримує профіль користувача і відображає його. Потрібно, щоб користувач був увійшов.

    Аргументи:
        request (HttpRequest): HTTP запит.
        user_id (int): Ідентифікатор користувача, чий профіль потрібно відобразити.

    Повертає:
        HttpResponse: Рендерить сторінку профілю користувача.
    """
    user = get_object_or_404(User, id=user_id)
    if request.user != user:
        messages.error(request, "Ви не маєте доступу до цього профілю.")
        return redirect('board:ad_list')

    profile = get_object_or_404(Profile, user=user)

    return render(request, 'board/profile.html',
                  {'user': user, 'profile': profile})


@login_required
def edit_profile_view(request, user_id: int):
    """
    View for editing the user profile.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders the profile edit page with a form.
    """
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(Profile, user=user)

    if request.user != user:
        return redirect('board:user_profile', user_id=request.user.id)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль успішно оновлено!")
            return redirect('board:user_profile', user_id=user.id)
        else:
            messages.error(request, "Будь ласка, виправте помилки у формі.")
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, "board/profile_edit.html", {"form": form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Оновлює сесію для користувача після зміни пароля
            messages.success(request, "Пароль успішно змінено.")
            return redirect('board:user_profile', user_id=request.user.id)  # Редірект на профіль користувача
        messages.error(request, "Не вдалося змінити пароль. Будь ласка, перевірте помилки.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'board/change_password.html', {'form': form})


class CustomLoginView(LoginView):
    """
    Custom login view that redirects the user to their profile page after successful login.

    Methods:
        get_success_url: Returns the URL to redirect the user to after a successful login.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Check if the user is already authenticated. If so, redirect them to their profile page.
        """
        if request.user.is_authenticated:
            # Redirect to the user's profile page if already logged in
            return redirect(reverse('board:user_profile', kwargs={'user_id': request.user.id}))

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        """
        Determines the URL to redirect to after successful login.

        Returns:
            str: The URL to the user's profile page.
        """
        return f'/board/profile/{self.request.user.id}/'


class CustomLogoutView(LogoutView):
    """
    Custom logout view that redirects the user to the main page after logout.

    Methods:
        get_logout_url: Returns the URL to redirect the user after logout.
    """

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        """
        Override the default GET method to add a success message and redirect
        the user after logging out.

        Returns:
            str: The URL to the main page.
        """
        messages.success(request, "Ви успішно вийшли з системи.")
        next_page = reverse_lazy('board:ad_list')  # Using reverse_lazy to get the URL dynamically
        return redirect(next_page)


def ad_statistics(request) -> render:
    """
    Displays statistics about advertisements and comments.

    Shows the number of ads created in the last month, the count of active and inactive ads,
    and the number of comments. It also displays the number of ads per category.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered statistics page with the ad statistics and category stats.
    """
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


@login_required
def delete_account_view(request, user_id):
    if request.user.id != user_id:
        raise Http404("Ви не маєте прав на видалення цього акаунта.")
    if request.method == "POST":
        request.user.delete()
        logout(request)
        return redirect("board:ad_list")
    return render(request, "board/delete_account.html", {'user_id': user_id})
