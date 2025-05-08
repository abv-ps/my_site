from channels.db import database_sync_to_async
from django.contrib.auth.models import User


@database_sync_to_async
def get_user_details(user_id):
    user = User.objects.filter(id=user_id).first()
    return {
        'username': user.username,
        'email': user.email
    }
