from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import Book

class BookAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_create_book(self):
        response = self.client.post('/books/', {
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Fiction',
            'publication_year': 2023
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_books(self):
        Book.objects.create(title="Book 1", author="Author 1", genre="Fiction", publication_year=2020, user=self.user)
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_books(self):
        Book.objects.create(title="Book 1", author="Author A", genre="Sci-Fi", publication_year=2021, user=self.user)
        response = self.client.get('/books/?author=Author A')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_books(self):
        Book.objects.create(title="Django Guide", author="John", genre="Tech", publication_year=2020, user=self.user)
        response = self.client.get('/books/?search=Django')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_delete_book(self):
        book = Book.objects.create(title="Book to Delete", author="John", genre="Tech", publication_year=2020, user=self.user)
        response = self.client.delete(f'/books/{book.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
