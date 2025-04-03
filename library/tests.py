"""
Tests for the Book API.

This module defines test cases for the Book API endpoints, ensuring that
the API behaves as expected for creating, listing, filtering, searching,
and deleting books.
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from .models import Book


class BookAPITest(APITestCase):
    """
    Test cases for the Book API.
    """

    def setUp(self) -> None:
        """
        Sets up the test environment by creating a test user and an admin user,
        and logging them in.
        """
        self.user: User = User.objects.create_user(username='testuser',
                                                   password='testpass')
        self.admin_user: User = User.objects.create_superuser(username='adminuser',
                                                              password='adminpass')
        self.client.login(username='testuser', password='testpass')

    def test_create_book(self) -> None:
        """
        Tests the creation of a book via the API.
        """
        response = self.client.post('/books/', {
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Fiction',
            'publication_year': 2023
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_books(self) -> None:
        """
        Tests the listing of books via the API.
        """
        Book.objects.create(title="Book 1", author="Author 1",
                            genre="Fiction", publication_year=2020,
                            user=self.user
                            )
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_books(self) -> None:
        """
        Tests the filtering of books by author via the API.
        """
        Book.objects.create(title="Book 1", author="Author A", genre="Sci-Fi",
                            publication_year=2021, user=self.user
                            )
        response = self.client.get('/books/?author=Author A')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_books(self) -> None:
        """
        Tests the searching of books by title via the API.
        """
        Book.objects.create(title="Django Guide", author="John", genre="Tech",
                            publication_year=2020, user=self.user
                            )
        response = self.client.get('/books/?search=Django')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_delete_book(self) -> None:
        """
        Tests the deletion of a book by an admin user via the API.
        """
        book: Book = Book.objects.create(title="Book to Delete", author="John",
                                         genre="Tech", publication_year=2020,
                                         user=self.user
                                         )
        self.client.logout()
        self.client.login(username='adminuser', password='adminpass')
        response = self.client.delete(f'/books/{book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_admin_delete_book(self) -> None:
        """
        Tests the deletion of a book by a non-admin user via the API.
        This should result in a 403 Forbidden response.
        """
        book: Book = Book.objects.create(title="Book to Delete", author="John",
                                         genre="Tech", publication_year=2020,
                                         user=self.user
                                         )
        response = self.client.delete(f'/books/{book.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self) -> None:
        """
        Test the update of a book
        """
        book: Book = Book.objects.create(title = "old title", author = "old author",
                                         genre = "old genre", publication_year = 2000,
                                         user = self.user
                                         )
        response = self.client.put(f'/books/{book.id}/', {
            'title': 'new title',
            'author': 'new author',
            'genre': 'new genre',
            'publication_year': 2024,
            'user': self.user.id
        }, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(id=book.id).title, 'new title')