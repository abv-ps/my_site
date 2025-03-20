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
from .models import Ad, Comment


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
