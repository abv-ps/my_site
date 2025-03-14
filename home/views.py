from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def home_view(request: HttpRequest) -> HttpResponse:
    """
    Renders the home page.

    Parameters:
        request (HttpRequest): The request object from the user.

    Returns:
        HttpResponse: The response containing the rendered home page template.
    """
    return render(request, 'home/home.html')


def about_view(request: HttpRequest) -> HttpResponse:
    """
    Renders the "About Us" page.

    Parameters:
        request (HttpRequest): The request object from the user.

    Returns:
        HttpResponse: The response containing the rendered "About Us" page template.
    """
    return render(request, 'home/about.html')


def contact_view(request: HttpRequest) -> HttpResponse:
    """
    Renders the "Contact Us" page.

    Parameters:
        request (HttpRequest): The request object from the user.

    Returns:
        HttpResponse: The response containing the rendered "Contact Us" page template.
    """
    return render(request, 'home/contact.html')


def post_view(request: HttpRequest, id: int) -> HttpResponse:
    """
    Renders the post page for a given post ID.

    Parameters:
        request (HttpRequest): The request object from the user.
        id (int): The ID of the post.

    Returns:
        HttpResponse: The response containing the rendered post page template with the given post ID.
    """
    return render(request, 'home/post.html', {'id': id})


def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    """
    Renders the user's profile page.

    Parameters:
        request (HttpRequest): The request object from the user.
        username (str): The username of the user.

    Returns:
        HttpResponse: The response containing the rendered profile page template with the user's name.
    """
    return render(request, 'home/profile.html', {'username': username})


def event_view(request: HttpRequest, year: int, month: int, day: int) -> HttpResponse:
    """
    Renders the event page for a given date.

    Parameters:
        request (HttpRequest): The request object from the user.
        year (int): The year of the event.
        month (int): The month of the event.
        day (int): The day of the event.

    Returns:
        HttpResponse: The response containing the rendered event page template with the given date.
    """
    return render(request, 'home/event.html', {'year': year, 'month': month, 'day': day})