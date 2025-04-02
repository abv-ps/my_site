"""
Module 'board.forms'

This module defines various forms used in the 'board' application.

It includes forms for:
- Creating and updating advertisements (`AdForm`).
- Posting comments on advertisements (`CommentForm`).
- User registration and profile creation (`RegistrationForm`).
- Updating user profile information (`UserProfileForm`).
- Changing user passwords (`PasswordChangeForm`).

These forms handle data validation, model interactions, and user input processing,
ensuring data integrity and providing a user-friendly interface for interacting
with the application's models.

Dependencies:
- django.forms: For form creation.
- django.contrib.auth: For user authentication and password management.
- django.core.exceptions: For custom validation errors.
- .models: For data models (Ad, Comment, Profile, Category).
- .validators: For custom data validation.
"""

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from django.core.exceptions import ValidationError

from .models import Ad, Comment, Profile, Category
from .validators import validate_avatar_image


class AdForm(forms.ModelForm):
    """
    A form for creating and updating Ad instances.

    This form is based on the `Ad` model and provides the necessary fields
    for creating or editing ads. The form includes fields such as title,
    description, price, and category.

    Attributes:
        existing_category (ChoiceField): A field to select an existing category.
        new_category (CharField): A field to create a new category.

        Meta:
            - model (Ad): Specifies the model to use for the form.
            - fields (list): A list of fields to include in the form.

    Methods:
        __init__: Initializes the form and sets the choices for the existing category field.
        clean: Cleans and validates the form data.
        save: Saves the form data and creates or updates an Ad instance.
    """
    existing_category = forms.ChoiceField(label="Вибрати категорію",
                                          choices=[], required=False)
    new_category = forms.CharField(label="Нова категорія", required=False)

    class Meta:
        #Metaclass for AdForm
        model = Ad
        fields = ['title', 'description', 'price', 'existing_category', 'new_category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes the form and sets the choices for the existing category field.
        """
        super().__init__(*args, **kwargs)
        if 'instance' not in kwargs or not kwargs['instance']:
            categories = Category.objects.all()
            self.fields['existing_category'].choices = (
                    [('', '---------')] + [(category.id, category.name)
                                           for category in categories]
            )

    def clean(self) -> dict:
        """
        Cleans and validates the form data.

        Returns:
            The cleaned form data.

        Raises:
            ValidationError: If neither existing category nor new category is provided,
                           or if both are provided, or if the new category name is empty,
                           or if the selected existing category does not exist.
        """
        cleaned_data = super().clean()
        existing_category = cleaned_data.get('existing_category')
        new_category = cleaned_data.get('new_category')

        if not existing_category and not new_category:
            self.add_error(None, "Виберіть існуючу категорію або створіть нову.")

        if existing_category and new_category:
            self.add_error(None, "Виберіть лише одну категорію.")

        if new_category:
            category_name = new_category.strip()
            if not category_name:
                self.add_error('new_category', "Назва нової категорії не може бути порожньою.")
            category, created = Category.objects.get_or_create(name=category_name)
            cleaned_data['category'] = category
        elif existing_category:
            try:
                cleaned_data['category'] = Category.objects.get(id=existing_category)
            except Category.DoesNotExist:
                self.add_error('existing_category', "Обрана категорія не існує.")

        return cleaned_data

    def save(self, commit: bool = True) -> Ad:
        """
        Saves the form data and creates or updates an Ad instance.

        Args:
            commit: Whether to save the instance to the database.

        Returns:
            The saved Ad instance.
        """
        instance = super().save(commit=False)
        if hasattr(self, 'cleaned_data') and 'category' in self.cleaned_data:
            instance.category = self.cleaned_data['category']
        if commit:
            instance.save()
        return instance


class CommentForm(forms.ModelForm):
    """
    A form for creating and updating Comment instances.

    This form is based on the `Comment` model and provides the necessary
    field for creating or editing comments. The form includes a content
    field for the comment's text.

    Attributes:
        Meta:
            - model (Comment): Specifies the model to use for the form.
            - fields (list): A list of fields to include in the form.
    """

    class Meta:
        #Metaclass for CommentForm
        model = Comment
        fields = ['content']


class RegistrationForm(forms.ModelForm):
    """
    A form for user registration, including user profile fields.

    This form collects standard user credentials along with profile details
    such as email, phone number, birth date, location, and avatar.

    Fields:
        username (CharField): Unique username for the user.
        email (EmailField): Unique email address.
        password1 (CharField): Primary password.
        password2 (CharField): Confirmation password.
        phone_number (CharField, optional): User's phone number.
        birth_date (DateField, optional): User's date of birth.
        location (CharField, optional): User's location.
        avatar (ImageField, optional): Profile avatar.

    Methods:
        clean_username: Ensures username uniqueness.
        clean_email: Ensures email uniqueness.
        clean: Ensures password confirmation.
        save: Creates a User and Profile instance.
    """

    username = forms.CharField(
        label="Логін",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Введіть логін"})
    )
    email = forms.EmailField(
        label="Електронна пошта",
        max_length=255,
        widget=forms.EmailInput(attrs={"placeholder": "Введіть електронну пошту"})
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Введіть пароль"}),
        min_length=8
    )
    password2 = forms.CharField(
        label="Повторіть пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Повторіть пароль"}),
        min_length=8
    )
    phone_number = forms.CharField(
        label="Номер телефону",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Введіть номер телефону"})
    )
    birth_date = forms.DateField(
        label="Дата народження",
        required=False,
        widget=forms.DateInput(attrs={"type": "date",
                                      "placeholder": "РРРР-ММ-ДД"})
    )
    location = forms.CharField(
        label="Адреса",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Введіть адресу"})
    )
    avatar = forms.ImageField(
        label="Аватар",
        required=False,
        validators=[validate_avatar_image],
        widget=forms.FileInput(attrs={"placeholder": "Виберіть аватар"})
    )

    class Meta:
        #Metaclass for RegistrationForm
        model = Profile
        fields = [
            "phone_number",
            "birth_date",
            "location",
            "avatar",
        ]

    def clean_username(self) -> str:
        """
        Ensures username uniqueness.

        Returns:
            The validated username.

        Raises:
            ValidationError: If a user with the given username already exists.
        """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Користувач із таким ім'ям вже існує.")
        return username

    def clean_email(self) -> str:
        """
        Ensures email uniqueness.

        Returns:
            The validated email.

        Raises:
            ValidationError: If the email is already in use.
        """
        email = self.cleaned_data.get("email")
        if (User.objects.filter(email=email).exists()
                or Profile.objects.filter(email=email).exists()):
            raise forms.ValidationError("Ця електронна пошта вже використовується.")
        return email

    def clean(self) -> dict:
        """
        Ensures password confirmation.

        Returns:
            The cleaned form data.

        Raises:
            ValidationError: If the passwords do not match.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Паролі не співпадають.")

        return cleaned_data

    def save(self, commit: bool = True) -> User:
        """
        Creates a new user and associated profile.

        The user password is securely hashed, and a profile is created with
        the additional fields provided in the form.

        Args:
            commit: Whether to save the instance to the database.

        Returns:
            The created User instance.
        """
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"]
        )
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone_number = self.cleaned_data.get("phone_number", "")
        profile.birth_date = self.cleaned_data.get("birth_date")
        profile.location = self.cleaned_data.get("location", "")
        profile.avatar = self.cleaned_data.get("avatar")

        if commit:
            profile.save()
        return user


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information, including avatar upload.

    Args:
        forms (ModelForm): Django form for user profile editing.

    Attributes:
        avatar (ImageField): Field for profile picture upload with size validation.
        email (EmailField): Field for user email.
        remove_avatar (BooleanField): Field for deleting user avatar.
        phone_number (CharField): Field for user phone number.
        birth_date (DateField): Field for user birth date.
        location (CharField): Field for user location.
    """
    email = forms.EmailField(required=False)
    remove_avatar = forms.BooleanField(label="Видалити аватар", required=False)

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes the form and sets the initial email value.
        """
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.email:
            self.fields["email"].initial = self.instance.email

    avatar = forms.ImageField(
        label="Аватар",
        required=False,
        validators=[validate_avatar_image],
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )

    phone_number = forms.CharField(label="Номер телефону", required=False)
    birth_date = forms.DateField(label="Дата народження", required=False,
                                 widget=forms.DateInput(attrs={'type': 'date'}))
    location = forms.CharField(label="Адреса", required=False)

    def clean_avatar(self) -> forms.ImageField:
        """
        Validate the uploaded avatar size.

        Returns:
            avatar: Validated avatar image.

        Raises:
            forms.ValidationError: If the file size exceeds 2MB.
        """
        avatar = self.cleaned_data.get("avatar")
        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Розмір файлу аватарки не повинен перевищувати 2 МБ.")
        return avatar

    class Meta:
        #Metaclass for UserProfileForm
        model = Profile
        fields = [
            "bio",
            "phone_number",
            "birth_date",
            "location",
            "is_active",
            "is_staff",
            "avatar",
            "remove_avatar"
        ]

    def save(self, commit: bool = True) -> Profile:
        """
        Saves the form data and updates the Profile instance.

        Args:
            commit: Whether to save the instance to the database.
            user: The user associated with the profile.

        Returns:
            The saved Profile instance.
        """
        instance = super().save(commit=False)
        if self.cleaned_data.get('remove_avatar'):
            instance.avatar.delete(save=False)
            instance.avatar = None
        if commit:
            instance.save()
        return instance


class PasswordChangeForm(DjangoPasswordChangeForm):
    """
    Form for changing user passwords.

    Args:
        DjangoPasswordChangeForm (Form): Base Django form for password change.

    Attributes:
        old_password (CharField): Field for the current password.
        new_password1 (CharField): Field for the new password.
        new_password2 (CharField): Field for confirming the new password.
    """
    old_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Current Password'})
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Confirm New Password'})
    )

    def clean_new_password1(self) -> str:
        """
        Validates the new password.

        Returns:
            The validated new password.

        Raises:
            ValidationError: If the password does not meet the validation criteria.
        """
        password1 = self.cleaned_data.get("new_password1")
        if password1:
            password_validation.validate_password(password1, self.user)
        return password1

    def clean_old_password(self) -> str:
        """
        Validates the old password.

        Returns:
            The validated old password.

        Raises:
            ValidationError: If the old password is incorrect.
        """
        old_password = self.cleaned_data.get('old_password')
        if not check_password(old_password, self.user.password):
            raise forms.ValidationError('Невірний поточний пароль.')
        return old_password

    def clean(self) -> dict:
        """
        Validates the form data and ensures password match.

        Returns:
            The cleaned form data.

        Raises:
            ValidationError: If the new password is the same as the old password,
                           or if the new passwords do not match.
        """
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password1 == old_password:
            self.add_error("new_password1", "Новий пароль повинен відрізнятися від старого.")

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error("new_password2", "Паролі не збігаються.")

        return cleaned_data
