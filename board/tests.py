from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from board.models import Category, Ad, Comment, Profile
from django.core import mail


class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="Транспорт")
        self.assertEqual(category.name, "Транспорт")


class AdModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.category = Category.objects.create(name="Нерухомість")

    def test_create_ad(self):
        ad = Ad.objects.create(
            title="Продам квартиру",
            description="Чудова квартира в центрі",
            price=100000,
            category=self.category,
            user=self.user
        )
        self.assertEqual(ad.title, "Продам квартиру")
        self.assertEqual(ad.price, 100000)
        self.assertEqual(ad.user.username, "testuser")

    def test_price_validator(self):
        ad = Ad(
            title="Недійсне оголошення",
            description="Тестове",
            price=-500,
            category=self.category,
            user=self.user
        )
        with self.assertRaises(ValidationError):
            ad.full_clean()


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser2", password="password")
        self.category = Category.objects.create(name="Авто")
        self.ad = Ad.objects.create(
            title="Продам авто",
            description="В гарному стані",
            price=5000,
            category=self.category,
            user=self.user
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            ad=self.ad,
            user=self.user,
            content="Цікавий варіант!"
        )
        self.assertEqual(comment.content, "Цікавий варіант!")
        self.assertEqual(comment.user.username, "testuser2")


class ProfileModelTest(TestCase):
    def test_create_profile(self):
        user = User.objects.create_user(username="profileuser", password="password")
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user.username, "profileuser")


class AdSignalsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="signaluser", password="password")
        self.category = Category.objects.create(name="Техніка")

    def send_email_on_ad_create(self):
        Ad.objects.create(
            title="Продам ноутбук",
            description="Майже новий",
            price=20000,
            category=self.category,
            user=self.user
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Ваше оголошення створено", mail.outbox[0].subject)

    def test_ad_deactivation_signal(self):
        ad = Ad.objects.create(
            title="Старий телевізор",
            description="Б/у",
            price=500,
            category=self.category,
            user=self.user,
            is_active=True
        )
        ad.is_active = False
        ad.save()
        self.assertFalse(Ad.objects.get(id=ad.id).is_active)
