from django.contrib.auth.models import User


def get_user(user_id):
    return User.objects.get(id=user_id)