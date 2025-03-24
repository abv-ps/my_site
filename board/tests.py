"""
This module contains test cases for the models in the `board` app of the Django project.

Test Cases:
- `CategoryModelTest`: Tests for the `Category` model functionality.
- `AdModelTest`: Tests for the `Ad` model functionality, including price validation.
- `CommentModelTest`: Tests for the `Comment` model functionality.
- `ProfileModelTest`: Tests for the `Profile` model functionality.
- `AdSignalsTest`: Tests for signals related to the `Ad` model, such as email notifications and deactivation signals.

The purpose of these tests is to ensure the correct creation, validation, and signal handling for the relevant models.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from board.models import Category, Ad, Comment, Profile
from django.core import mail


class CategoryModelTest(TestCase):
    """
    Test case for the `Category` model.

    This test case ensures the correct creation and functionality of `Category` objects.

    Methods:
        test_create_category: Tests that a category can be created with a name and that
        the name is correctly set.
    """

    def test_create_category(self) -> None:
        """
        Tests the creation of a `Category` instance.

        Ensures that a category can be created and its `name` attribute is correctly set.
        """
        category = Category.objects.create(name="Транспорт")
        self.assertEqual(category.name, "Транспорт")


class AdModelTest(TestCase):
    """
    Test case for the `Ad` model.

    This test case ensures the correct creation and validation of `Ad` objects,
    including price validation.

    Methods:
        test_create_ad: Tests that an ad can be created with the correct attributes.
        test_price_validator: Tests that an ad's price cannot be negative.
    """

    def setUp(self) -> None:
        """
        Set up the necessary data for the `Ad` model tests.

        This method creates a user and a category instance for the subsequent tests.
        """
        self.user = User.objects.create_user(username="testuser", password="password")
        self.category = Category.objects.create(name="Нерухомість")

    def test_create_ad(self) -> None:
        """
        Tests the creation of an `Ad` instance.

        Ensures that an ad can be created with the correct attributes such as title,
        description, price, category, and user.
        """
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

    def test_price_validator(self) -> None:
        """
        Tests the price validation in the `Ad` model.

        Ensures that an `Ad` with a negative price raises a `ValidationError`.
        """
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
    """
    Test case for the `Comment` model.

    This test case ensures the correct creation and functionality of `Comment` objects.

    Methods:
        test_create_comment: Tests that a comment can be created and associated with an ad.
    """

    def setUp(self) -> None:
        """
        Set up the necessary data for the `Comment` model tests.

        This method creates a user, a category, and an ad instance for the subsequent tests.
        """
        self.user = User.objects.create_user(username="testuser2", password="password")
        self.category = Category.objects.create(name="Авто")
        self.ad = Ad.objects.create(
            title="Продам авто",
            description="В гарному стані",
            price=5000,
            category=self.category,
            user=self.user
        )

    def test_create_comment(self) -> None:
        """
        Tests the creation of a `Comment` instance.

        Ensures that a comment can be created with a specified content and associated with a user and ad.
        """
        comment = Comment.objects.create(
            ad=self.ad,
            user=self.user,
            content="Цікавий варіант!"
        )
        self.assertEqual(comment.content, "Цікавий варіант!")
        self.assertEqual(comment.user.username, "testuser2")


class ProfileModelTest(TestCase):
    """
    Test case for the `Profile` model.

    This test case ensures that a user profile can be correctly created.

    Methods:
        test_create_profile: Tests that a user profile is created when a user is created.
    """

    def test_create_profile(self) -> None:
        """
        Tests the automatic creation of a `Profile` instance when a user is created.

        Ensures that the profile is correctly associated with the user.
        """
        user = User.objects.create_user(username="profileuser", password="password")
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user.username, "profileuser")


class AdSignalsTest(TestCase):
    """
    Test case for testing signals associated with the `Ad` model.

    This test case ensures that signals related to ad creation and deactivation work correctly.

    Methods:
        send_email_on_ad_create: Tests that an email is sent when an ad is created.
        test_ad_deactivation_signal: Tests that deactivating an ad updates its status.
    """

    def setUp(self) -> None:
        """
        Set up the necessary data for testing signals related to the `Ad` model.

        This method creates a user and a category instance for the subsequent tests.
        """
        self.user = User.objects.create_user(username="signaluser", password="password")
        self.category = Category.objects.create(name="Техніка")

    def send_email_on_ad_create(self) -> None:
        """
        Tests that an email is sent when an ad is created.

        Ensures that the email subject contains a notification about ad creation.
        """
        Ad.objects.create(
            title="Продам ноутбук",
            description="Майже новий",
            price=20000,
            category=self.category,
            user=self.user
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Ваше оголошення створено", mail.outbox[0].subject)

    def test_ad_deactivation_signal(self) -> None:
        """
        Tests that deactivating an ad triggers the expected changes.

        Ensures that the ad's `is_active` field is updated correctly when the ad is deactivated.
        """
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

class UserProfileFormTest(TestCase):
    """
    Tests for the UserProfileForm.
    """

    def setUp(self):
        """
        Set up a test user and profile.
        """
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.profile = UserProfile.objects.create(user=self.user, phone_number="123456789", address="Test Address")

    def test_valid_form(self):
        """
        Test that a valid form saves correctly.
        """
        form_data = {
            "phone_number": "987654321",
            "address": "New Address"
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_number(self):
        """
        Test that an invalid phone number does not pass validation.
        """
        form_data = {
            "phone_number": "invalid_phone",
            "address": "Some Address"
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertFalse(form.is_valid())

    def test_upload_avatar(self):
        """
        Test that an image can be uploaded as an avatar.
        """
        image = SimpleUploadedFile("avatar.jpg", b"file_content", content_type="image/jpeg")
        form_data = {
            "phone_number": "987654321",
            "address": "New Address"
        }
        form = UserProfileForm(data=form_data, files={"avatar": image}, instance=self.profile)
        self.assertTrue(form.is_valid())

class EditProfileViewTest(TestCase):
    """
    Tests for the edit_profile view.
    """

    def setUp(self):
        """
        Set up a test user and log them in.
        """
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        self.profile = UserProfile.objects.create(user=self.user, phone_number="123456789", address="Test Address")

    def test_get_edit_profile_page(self):
        """
        Test that the edit profile page loads correctly.
        """
        response = self.client.get(reverse("board:edit_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Редагування профілю")

    def test_post_valid_edit_profile(self):
        """
        Test submitting a valid form updates the profile.
        """
        response = self.client.post(reverse("board:edit_profile"), {
            "phone_number": "987654321",
            "address": "Updated Address"
        })
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone_number, "987654321")
        self.assertEqual(self.profile.address, "Updated Address")
        self.assertRedirects(response, reverse("board:profile"))

    def test_post_invalid_edit_profile(self):
        """
        Test that submitting an invalid form does not update the profile.
        """
        response = self.client.post(reverse("board:edit_profile"), {
            "phone_number": "invalid_phone",
            "address": "Updated Address"
        })
        self.profile.refresh_from_db()
        self.assertNotEqual(self.profile.phone_number, "invalid_phone")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Будь ласка, виправте помилки у формі.")
