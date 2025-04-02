"""
Module 'board.views'

This module defines the views for the bulletin board application. It handles user
authentication, profile management, advertisement management, and statistics.

Key Views:

- **register_view**: Handles user registration, displaying the registration form and
  creating new users.

- **ad_list**: Displays a list of active advertisements.

- **ad_detail**: Displays the details of a specific advertisement and handles comment
  submission.

- **user_profile**: Displays the user's profile. Requires the user to be logged in.

- **edit_profile_view**: Allows users to edit their profiles.

- **change_password_view**: Allows users to change their passwords.

- **CustomLoginView**: Custom login view that redirects users to their profile page
  after successful login.

- **CustomLogoutView**: Custom logout view that redirects users to the main page
  after logout.

- **ad_statistics**: Displays statistics about advertisements and comments.

- **delete_account_view**: Allows users to delete their accounts.

- **add_ad**: Allows users to add new advertisements.

Dependencies:
- django.shortcuts
- django.contrib.messages
- django.contrib.auth
- django.http
- django.urls
- django.utils
- datetime
- django.db.models
- .models
- .forms
"""
from typing import Any
from datetime import timedelta

from django.http import HttpResponse, HttpRequest, Http404, HttpResponseBase
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Count

from .models import Ad, User, Category, Comment, Profile
from .forms import CommentForm, RegistrationForm, UserProfileForm, PasswordChangeForm, AdForm


def register_view(request: HttpRequest) -> HttpResponse:
    """
    Handles user registration.

    Displays the registration form and creates a new user upon form submission.
    Redirects the user to the login page upon successful registration.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered registration page or a redirect to the login page if the form is valid.
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
        return render(request, 'registration/register.html', {'form': form})
    form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def ad_list(request: HttpRequest) -> HttpResponse:
    """
    Displays the list of active advertisements.

    Fetches all active advertisements and renders them in the ad list page.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered ad list page with the active ads.
    """
    ads = Ad.objects.filter(is_active=True)
    return render(request, 'board/ad_list.html', {'ads': ads})


def ad_detail(request: HttpRequest, ad_id: int) -> HttpResponse:
    """
    Displays the details of a specific advertisement and handles comment submission.

    Fetches the advertisement by its ID, displays its details, and allows users to add comments.

    Args:
        request: The HTTP request object.
        ad_id: The ID of the advertisement to display.

    Returns:
        The rendered ad detail page with the ad's information and comments.
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
def user_profile(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    Displays the user profile.

    Retrieves and displays the user's profile. Requires the user to be logged in.

    Args:
        request: The HTTP request object.
        user_id: The ID of the user whose profile to display.

    Returns:
        The rendered user profile page.
    """
    user = get_object_or_404(User, id=user_id)
    if request.user != user:
        messages.error(request, "Ви не маєте доступу до цього профіля.")
        return redirect('board:ad_list')

    profile = get_object_or_404(Profile, user=user)

    return render(request, 'board/profile.html',
                  {'user': user, 'profile': profile})


@login_required
def edit_profile_view(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    View for editing the user profile.

    Args:
        request: The request object.
        user_id: The ID of the user whose profile to edit.

    Returns:
        The rendered profile edit page with a form.
    """
    user = get_object_or_404(User, id=user_id)
    _user_profile = get_object_or_404(Profile, user=user)

    if request.user != user:
        return redirect('board:user_profile', user_id=request.user.id)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=_user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль успішно оновлено!")
            return redirect('board:user_profile', user_id=user.id)
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Помилка в полі '{field}': {error}")
        messages.error(request, "Будь ласка, виправте помилки у формі.")
    else:
        form = UserProfileForm(instance=_user_profile)

    return render(request, "board/profile_edit.html",
                  {"form": form, "user_id": user_id})


@login_required
def change_password_view(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    View for changing the user's password.

    Args:
        request: The request object.
        user_id: The ID of the user whose password to change.

    Returns:
        The rendered password change page with a form.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Пароль успішно змінено.")
            return redirect('board:user_profile', user_id=request.user.id)
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Помилка в полі '{field}': {error}")
        messages.error(request, "Не вдалося змінити пароль. Будь ласка, перевірте помилки.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'board/change_password.html',
                  {'form': form, "user_id": user_id})


class CustomLoginView(LoginView):
    """
    Custom login view that redirects the user to their profile page after successful login.

    Methods:
        get_success_url: Returns the URL to redirect the user to after a successful login.
    """

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        """
        Redirects authenticated users to their profile page before handling the request.

        If the user is already logged in, they are redirected to their profile instead of
        accessing this view.

        Args:
            request (HttpRequest): The incoming HTTP request.
            *args (Any): Additional positional arguments.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            HttpResponse: A redirect response if the user is authenticated,
                          otherwise the regular view response.
        """
        if request.user.is_authenticated:
            return redirect('board:user_profile', user_id=request.user.id)

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        """
        Determines the URL to redirect to after successful login.

        Returns:
            The URL to the user's profile page.
        """
        return f'/board/profile/{self.request.user.id}/'


class CustomLogoutView(LogoutView):
    """
    Custom logout view that redirects the user to the main page after logout.

    Methods:
        get: Overrides the default GET method to add a success message and redirect.
    """

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        """
        Override the default GET method to add a success message and redirect
        the user after logging out.

        Returns:
            The URL to the main page.
        """
        messages.success(request, "Ви успішно вийшли з системи.")
        next_page = reverse_lazy('board:ad_list')
        return redirect(next_page)


def ad_statistics(request: HttpRequest) -> HttpResponse:
    """
    Displays statistics about advertisements and comments.

    Shows the number of ads created in the last month, the count of active and inactive ads,
    and the number of comments. It also displays the number of ads per category.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered statistics page with the ad statistics and category stats.
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
def delete_account_view(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    View for deleting a user account.

    Args:
        request: The HTTP request object.
        user_id: The ID of the user whose account to delete.

    Returns:
        The rendered delete account confirmation page or a redirect to the ad list.
    """
    if request.user.id != user_id:
        raise Http404("Ви не маєте прав на видалення цього акаунта.")
    if request.method == "POST":
        request.user.delete()
        logout(request)
        return redirect("board:ad_list")
    return render(request, "board/delete_account.html", {'user_id': user_id})


@login_required
def add_ad(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    View for adding a new advertisement.

    Args:
        request: The HTTP request object.
        user_id: The ID of the user adding the advertisement.

    Returns:
        The rendered add advertisement form or a redirect to the user profile.
    """
    user = get_object_or_404(User, id=user_id)
    if request.user != user:
        messages.error(request, "Ви не можете додавати оголошення до чужого профілю.")
        return redirect('board:user_profile', user_id=user.id)

    if request.method == "POST":
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            category = form.cleaned_data.get('category')
            if not category:
                messages.error(request, "Категорія не була вибрана або створена.")
                return render(request, 'board/add_ad.html', {'form': form, 'user_id': user_id})
            ad.category = category
            ad.save()
            messages.success(request, "Оголошення успішно додано!")
            return redirect('board:user_profile', user_id=user.id)
        for errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Помилка: {error}")
        messages.error(request, "Будь ласка, виправте помилки у формі.")
    else:
        form = AdForm()

    return render(request, 'board/add_ad.html', {'form': form, 'user_id': user_id})
