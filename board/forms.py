"""
This module contains forms for creating and updating `Ad` and `Comment`
instances in the 'board' application.

The forms are based on Django's `ModelForm` class and provide a convenient
way to interact with the `Ad` and `Comment` models through HTML forms.

Module Dependencies:
- `django.forms`: For creating model forms.
- `.models`: For importing the `Ad` and `Comment` models.

Forms:
    - AdForm: A form for creating and updating `Ad` instances. It includes fields
      such as `title`, `description`, `price`, and `category`.
    - CommentForm: A form for creating and updating `Comment` instances. It includes
      the `content` field for the comment text.

"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from .models import Ad, Comment
from .models import Profile


class AdForm(forms.ModelForm):
    """
    A form for creating and updating Ad instances.

    This form is based on the `Ad` model and provides the necessary fields
    for creating or editing ads. The form includes fields such as title,
    description, price, and category.

    Attributes:
        Meta:
            - model: Specifies the model to use for the form (Ad).
            - fields: A list of fields to include in the form.

    Methods:
        None
    """

    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'category']


class CommentForm(forms.ModelForm):
    """
   A form for creating and updating Comment instances.

   This form is based on the `Comment` model and provides the necessary
   field for creating or editing comments. The form includes a content
   field for the comment's text.

   Attributes:
       Meta:
           - model: Specifies the model to use for the form (Comment).
           - fields: A list of fields to include in the form.

   Methods:
       None
   """

    class Meta:
        model = Comment
        fields = ['content']

class RegistrationForm(forms.ModelForm):
    """
    A form for user registration, including user profile fields.

    This form collects standard user credentials along with profile details
    such as email, phone number, birth date, location, and avatar.

    Fields:
        username (str): Unique username for the user.
        email (EmailField): Unique email address.
        password1 (str): Primary password.
        password2 (str): Confirmation password.
        phone_number (str, optional): User's phone number.
        birth_date (date, optional): User's date of birth.
        location (str, optional): User's location.
        avatar (ImageField, optional): Profile avatar.

    Methods:
        clean_email: Ensures email uniqueness.
        clean: Ensures password confirmation.
        save: Creates a User and Profile instance.
    """

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput, min_length=8
    )
    password2 = forms.CharField(
        label="Повторіть пароль",
        widget=forms.PasswordInput, min_length=8
    )
    phone_number = forms.CharField(
        label="Номер телефону",
        max_length=20,
        required=False
    )
    birth_date = forms.DateField(
        label="Дата народження",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )
    location = forms.CharField(
        label="Адреса",
        max_length=255,
        required=False
    )
    avatar = forms.ImageField(
        label="Аватар",
        required=False
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Користувач із таким ім'ям вже існує.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists() or Profile.objects.filter(email=email).exists():
            raise forms.ValidationError("Ця електронна пошта вже використовується.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Паролі не співпадають.")

        return cleaned_data

    def save(self, commit=True):
        """
        Creates a new user and associated profile.

        The user password is securely hashed, and a profile is created with
        the additional fields provided in the form.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data.get("phone_number", ""),
                birth_date=self.cleaned_data.get("birth_date"),
                location=self.cleaned_data.get("location", ""),
                email=self.cleaned_data.get("email"),
                avatar=self.cleaned_data.get("avatar")
            )
        return user


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information, including avatar upload.

    Args:
        forms (ModelForm): Django form for user profile editing.

    Attributes:
        avatar (ImageField): Field for profile picture upload with size validation.
    """

    def clean_avatar(self):
        """
        Validate the uploaded avatar size.

        Returns:
            avatar: Validated avatar image.

        Raises:
            forms.ValidationError: If the file size exceeds 2MB.
        """
        avatar = self.cleaned_data.get("avatar")
        if avatar and avatar.size > 2 * 1024 * 1024:  # 2MB limit
            raise forms.ValidationError("The avatar file size must not exceed 2MB.")
        return avatar

    class Meta:
        model = Profile
        fields = [
            "bio",
            "phone_number",
            "birth_date",
            "location",
            "email",
            "is_active",
            "is_staff",
            "avatar"
        ]


class PasswordChangeForm(DjangoPasswordChangeForm):
    old_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'})
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'})
    )

    def clean_new_password1(self):
        password1 = self.cleaned_data.get("new_password1")
        if password1:
            password_validation.validate_password(password1, self.user)
        return password1

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not check_password(old_password, self.user.password):
            raise forms.ValidationError('Incorrect current password.')
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password1 == old_password:
            self.add_error("new_password1", "The new password must be different from the old one.")

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error("new_password2", "Passwords do not match.")

        return cleaned_data