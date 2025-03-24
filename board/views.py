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

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from .models import Ad, User, Category, Comment, Profile
from .forms import CommentForm, RegistrationForm


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
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Ваш акаунт успішно створено!')
            login(request, user)
            return redirect('board:login')
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
def user_profile(request, username: str) -> render:
    """
    Displays the profile of a user.

    Fetches the user's profile and displays it. Requires the user to be logged in.

    Args:
        request (HttpRequest): The HTTP request object.
        username (str): The username of the user whose profile to display.

    Returns:
        HttpResponse: The rendered user profile page.
    """
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'board/profile.html', {'user': user, 'profile': profile})


@login_required
def edit_profile(request):
    """
    View for editing the user profile.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders the profile edit page with a form.
    """
    user_profile = request.user.profile

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль успішно оновлено!")
            return redirect("board:profile")
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
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect('board: profile')
        messages.error(request, "Failed to change password. Please check the errors.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


class CustomLoginView(LoginView):
    """
    Custom login view that redirects the user to their profile page after successful login.

    Methods:
        get_success_url: Returns the URL to redirect the user to after a successful login.
    """

    def get_success_url(self) -> str:
        """
        Determines the URL to redirect to after successful login.

        Returns:
            str: The URL to the user's profile page.
        """
        print(f"Redirecting to profile for user {self.request.user.username}")
        return f'/board/profile/{self.request.user.username}/'


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
def delete_account_view(request):
    if request.method == "POST":
        request.user.delete()
        logout(request)
        return redirect("board:ad_list")
    return render(request, "board/delete_account.html")
