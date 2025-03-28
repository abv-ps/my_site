"""
Module: test_views.py

This module contains test cases for various views and forms within the application.
Each test case ensures that the corresponding view or form behaves as expected,
handling both valid and invalid inputs and interactions.

Test Cases:
    1. `CategoryModelTest`: Tests the functionality and creation of the `Category` model.
    2. `AdModelTest`: Tests the creation and validation of `Ad` objects,
       including price validation.
    3. `CommentModelTest`: Tests the functionality of the `Comment` model
       and its association with `Ad` objects.
    4. `ProfileModelTest`: Ensures that user profiles are created
       and associated with users correctly.
    5. `AdSignalsTest`: Tests the signals related to the `Ad` model,
       including email notifications and ad deactivation.
    6. `UserProfileFormTest`: Tests for the validation, submission,
       and file upload functionality of the `UserProfileForm`.
    7. `EditProfileViewTest`: Tests the behavior of the `edit_profile` view,
    including GET and POST requests for editing a user profile.

Each test case follows the standard Django `TestCase` pattern to test specific aspects
of the models, views, and forms. They verify that data is correctly handled,
validations are applied, and proper responses are returned for various interactions.

Modules and Dependencies:
    - `django.test.TestCase`: The base class for all test cases in Django,
       providing methods for sending requests, asserting responses,
       and managing test setup/teardown.
    - `django.urls.reverse`: Used to generate URLs for views based
       on their names and parameters.
    - `django.core.files.uploadedfile.SimpleUploadedFile`: Used to simulate file uploads
       in the tests.
    - `PIL.Image`: Used for generating images in the avatar upload test.
    - `django.db.models.signals.post_save`: Used for connecting and disconnecting
    signals related to model changes.

Each class includes setup and teardown methods to ensure that tests run
in an isolated environment and do not interfere with each other.
Additionally, the tests follow best practices for checking edge cases,
such as invalid form submissions, and confirm that the application responds as expected.

Test cases are self-contained and are intended to verify that the individual components
of the application work independently and together as expected.
"""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.signals import post_save
from .signals import create_user_profile, save_user_profile
from django.shortcuts import reverse
from django.test import TestCase
from PIL import Image
import io
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .forms import UserProfileForm
from .models import Category, Ad, Comment, Profile
from django.core import mail


class CategoryModelTest(TestCase):
    """
    Test case for the `Category` model.

    This test case ensures the correct creation and functionality
    of `Category` objects.

    Attributes:
        None

    Methods:
        test_create_category:
            Tests that a category can be created with a name and that
            the name is correctly set.
    """

    def test_create_category(self) -> None:
        """
        Tests the creation of a `Category` instance.

        Ensures that a category can be created and its `name` attribute
        is correctly set.

        This method performs the following actions:
            - Creates a `Category` instance with the name "Транспорт".
            - Asserts that the `name` attribute of the created category
            is equal to "Транспорт".

        Returns:
            None
        """
        category = Category.objects.create(name="Транспорт")
        self.assertEqual(category.name, "Транспорт")


class AdModelTest(TestCase):
    """
    Test case for the `Ad` model.

    This test case ensures the correct creation and validation of `Ad` objects,
    including price validation.

    Attributes:
        user (User): A test user to associate with the ad.
        category (Category): A test category to associate with the ad.

    Methods:
        test_create_ad:
            Tests that an ad can be created with the correct attributes
            such as title, description, price, category, and user.

        test_price_validator:
            Tests that an ad's price cannot be negative, raising
            a `ValidationError`.
    """

    def setUp(self) -> None:
        """
        Set up the necessary data for the `Ad` model tests.

        This method creates a user and a category instance
        for the subsequent tests.

        Returns:
            None
        """
        self.user = User.objects.create_user(username="testuser",
                                             password="password")
        self.category = Category.objects.create(name="Нерухомість")

    def test_create_ad(self) -> None:
        """
        Tests the creation of an `Ad` instance.

        Ensures that an ad can be created with the correct attributes
        such as title, description, price, category, and user.

        Returns:
            None
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

        Ensures that an `Ad` with a negative price raises
        a `ValidationError`.

        Returns:
            None
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

    This test case ensures the correct creation and functionality
    of `Comment` objects.

    Attributes:
        user (User): A test user to associate with the comment.
        category (Category): A test category to associate with the ad.
        ad (Ad): A test ad to associate with the comment.

    Methods:
        test_create_comment:
            Tests that a comment can be created and associated with an ad.
    """

    def setUp(self) -> None:
        """
        Set up the necessary data for the `Comment` model tests.

        This method creates a user, a category, and an ad instance
        for the subsequent tests.

        Returns:
            None
        """
        self.user = User.objects.create_user(username="testuser2",
                                             password="password")
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

        Ensures that a comment can be created with a specified content
        and associated with a user and ad.

        This method performs the following actions:
            - Creates a `Comment` instance with the given content, user,
              and associated ad.
            - Asserts that the content of the comment is correctly set.
            - Asserts that the user associated with the comment is the correct one.

        Returns:
            None
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

    Attributes:
        None

    Methods:
        test_create_profile:
            Tests that a user profile is created when a user is created
            and is correctly associated with the user.
    """

    def test_create_profile(self) -> None:
        """
        Tests the automatic creation of a `Profile` instance when a user is created.

        Ensures that the profile is correctly associated with the user.

        This method performs the following actions:
            - Creates a new user instance.
            - Retrieves the associated `Profile` instance.
            - Asserts that the profile is correctly linked to the user.

        Returns:
            None
        """
        user = User.objects.create_user(username="profileuser",
                                        password="password")
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user.username, "profileuser")


class AdSignalsTest(TestCase):
    """
    Test case for testing signals associated with the `Ad` model.

    This test case ensures that signals related to ad creation
    and deactivation work correctly.

    Attributes:
        user (User): A test user to associate with the ad.
        category (Category): A test category to associate with the ad.

    Methods:
        send_email_on_ad_create:
            Tests that an email is sent when an ad is created, and the email subject
            contains a notification.

        test_ad_deactivation_signal:
            Tests that deactivating an ad updates its status correctly.
    """

    def setUp(self) -> None:
        """
        Set up the necessary data for testing signals related to the `Ad` model.

        This method creates a user and a category instance for the subsequent tests.

        Returns:
            None
        """
        self.user = User.objects.create_user(username="signaluser",
                                             password="password")
        self.category = Category.objects.create(name="Техніка")

    def send_email_on_ad_create(self) -> None:
        """
        Tests that an email is sent when an ad is created.

        Ensures that the email subject contains a notification about ad creation.

        This method performs the following actions:
            - Creates a new `Ad` instance.
            - Asserts that an email is sent and its subject contains
            the phrase "Ваше оголошення створено".

        Returns:
            None
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

        Ensures that the ad's `is_active` field is updated correctly
        when the ad is deactivated.

        This method performs the following actions:
            - Creates a new `Ad` instance with `is_active=True`.
            - Sets the ad's `is_active` field to `False` and saves it.
            - Asserts that the ad's `is_active` field is updated correctly.

        Returns:
            None
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
    Test case for testing the `UserProfileForm`.

    This test case ensures the correct functionality of the `UserProfileForm`
    by testing valid and invalid data, as well as file uploads.

    Attributes:
        user (User): A test user instance.
        profile (Profile): A test profile instance associated with the user.

    Methods:
        test_valid_form:
            Tests that a valid `UserProfileForm` saves correctly.

        test_invalid_phone_number:
            Tests that an invalid phone number fails validation.

        test_upload_avatar:
            Tests that an image file can be uploaded as an avatar.
    """

    def setUp(self) -> None:
        """
        Set up a test user and profile.

        This method disconnects the signals for profile creation
        and saving during setup to prevent them from interfering with the test.
        It creates a user and a profile for use in the test cases.

        Returns:
            None
        """
        post_save.disconnect(create_user_profile, sender=User)
        post_save.disconnect(save_user_profile, sender=User)

        self.user = User.objects.create_user(username="testuser",
                                             password="password123")
        self.profile = Profile.objects.create(user=self.user,
                                              phone_number="+380961231122",
                                              location="Test Address",
                                              email="test@email.com")

    def tearDown(self) -> None:
        """
        Restore the signals after the test.

        This method reconnects the signals for profile creation
        and saving to ensure normal operation
        after the tests are completed.

        Returns:
            None
        """
        post_save.connect(create_user_profile, sender=User)
        post_save.connect(save_user_profile, sender=User)

    def test_valid_form(self) -> None:
        """
        Test that a valid form saves correctly.

        This method tests that a form with valid data can
        be successfully validated and saved.

        Returns:
            None
        """
        form_data = {
            "phone_number": "+380961231122",
            "email": "test@email.com",
            "location": "New Address"
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_number(self) -> None:
        """
        Test that an invalid phone number does not pass validation.

        This method ensures that the form rejects an invalid phone number
        and adds errors to the form.

        Returns:
            None
        """
        form_data = {
            "phone_number": "invalid_phone",
            "email": "test@email.com",
            "location": "Some Address"
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertTrue(form.errors['phone_number'])

    def test_upload_avatar(self) -> None:
        """
        Test that an image can be uploaded as an avatar.

        This method tests that an image file can be uploaded
        as the avatar field in the profile form.

        Returns:
            None
        """
        image = Image.new('RGB', (100, 100), color='red')
        image_file = io.BytesIO()
        image.save(image_file, 'JPEG')
        image_file.name = 'avatar.jpg'
        image_file.seek(0)
        uploaded_file = SimpleUploadedFile("avatar.jpg",
                                           image_file.getvalue(),
                                           content_type="image/jpeg")

        form_data = {
            "phone_number": "+380961231122",
            "email": "test@email.com",
            "location": "New Address"
        }
        form = UserProfileForm(data=form_data,
                               files={"avatar": uploaded_file},
                               instance=self.profile)
        self.assertTrue(form.is_valid(), f"Form is invalid. "
                                         f"Errors: {form.errors}")
        self.assertEqual(form.cleaned_data['avatar'].name, 'avatar.jpg')


class EditProfileViewTest(TestCase):
    """
    Test case for testing the `edit_profile` view.

    This test case ensures that the edit profile page functions correctly,
    including displaying the page, handling valid form submissions,
    and preventing invalid form submissions.

    Attributes:
        user (User): A test user instance to be used for the profile.
        profile (Profile): A test profile instance associated with the user.

    Methods:
        test_get_edit_profile_page:
            Tests that the edit profile page loads correctly.

        test_post_valid_edit_profile:
            Tests that submitting a valid form updates the profile.

        test_post_invalid_edit_profile:
            Tests that submitting an invalid form does not update the profile.
    """

    def setUp(self) -> None:
        """
        Set up a test user and log them in.

        This method disconnects signals for user profile creation
        and saving, then creates a test user,
        logs them in, and creates a profile associated with the user.

        Returns:
            None
        """
        post_save.disconnect(create_user_profile, sender=User)
        post_save.disconnect(save_user_profile, sender=User)

        self.user = User.objects.create_user(username="testuser",
                                             password="password123")
        self.client.login(username="testuser", password="password123")
        self.profile = Profile.objects.create(user=self.user,
                                              phone_number="+380961231122",
                                              location="Test Address",
                                              email="test@email.com")

    def tearDown(self) -> None:
        """
        Restore the signals after the test.

        This method reconnects the signals for user profile creation
        and saving after the tests are done.

        Returns:
            None
        """
        post_save.connect(create_user_profile, sender=User)
        post_save.connect(save_user_profile, sender=User)

    def test_get_edit_profile_page(self) -> None:
        """
        Test that the edit profile page loads correctly.

        This method sends a GET request to the edit profile page and checks that:
            - The status code of the response is 200 (OK).
            - The page contains the text "Редагування профілю" (Edit Profile).

        Returns:
            None
        """
        user_id = self.user.id
        response = self.client.get(reverse("board:edit_profile",
                                           kwargs={"user_id": user_id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Редагування профілю")

    def test_post_valid_edit_profile(self) -> None:
        """
        Test submitting a valid form updates the profile.

        This method sends a POST request with valid form data
        to the edit profile page and checks that:
            - The profile is updated with the new values
              for phone number and location.
            - The user is redirected to their user profile page.

        Returns:
            None
        """
        user_id = self.user.id
        response = self.client.post(
            reverse("board:edit_profile", kwargs={"user_id": user_id}),
            {
                "phone_number": "+380961231231",
                "location": "Updated Address"
            }
        )
        self.profile = Profile.objects.get(user=self.user)
        self.assertEqual(self.profile.phone_number, "+380961231231")
        self.assertEqual(self.profile.location, "Updated Address")
        self.assertRedirects(response, reverse("board:user_profile",
                                               kwargs={"user_id": user_id}))

    def test_post_invalid_edit_profile(self) -> None:
        """
        Test that submitting an invalid form does not update the profile.

        This method sends a POST request with invalid form data
        (invalid phone number) and checks that:
            - The profile's phone number is not updated.
            - The page reloads with an error message indicating the form is invalid.

        Returns:
            None
        """
        user_id = self.user.id
        response = self.client.post(reverse("board:edit_profile",
                                            kwargs={"user_id": user_id}), {
                                        "phone_number": "invalid_phone",
                                        "location": "Updated Address"
                                    })
        self.profile = Profile.objects.get(user=self.user)
        self.assertNotEqual(self.profile.phone_number, "invalid_phone")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Будь ласка, виправте помилки у формі.")
