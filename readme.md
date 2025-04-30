# The site to display Django's core practices

## Initial project setup

1. **Create a `.env` file** in the root directory with the following keys:
    DJANGO_SECRET_KEY=your_key
    DJANGO_DEBUG=True (for local development)
    POSTGRES_DB=name_your_db
    POSTGRES_USER=your_user
    POSTGRES_PASSWORD=your_password
    POSTGRES_HOST=custom_postgres
    POSTGRES_PORT=some_port


2. **Create a superuser (optional):**

You can create one manually via shell:

```docker-compose exec web python manage.py shell
from django.contrib.auth.models import User
user = User.objects.create_user(
    username="admin",
    email="admin@example.com",
    password="your_password",
    is_staff=True,
    is_superuser=True
)
user.save()
```

## To up the project

docker-compose up --build

The application will be available at: http://localhost:8000

Uploaded media (e.g. images via ImageField) will be stored in a Docker volume (media_data), mapped to /app/media/ inside the container.