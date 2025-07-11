# The site to display Django's core practices

## Initial project setup

1. **Create a `.env` file** in the root directory with the following keys:
    <pre> 
    DJANGO_SECRET_KEY=your_key
    DJANGO_DEBUG=True (for local development)

    POSTGRES_DB=name_your_db
    POSTGRES_USER=your_user
    POSTGRES_PASSWORD=your_password
    POSTGRES_HOST=custom_postgres
    POSTGRES_PORT=5432
   </pre>
   <strong>RabbitMQ (for Celery)</strong>
    <pre>
    RABBITMQ_USER=my_user 
    RABBITMQ_PASSWORD=my_password
    RABBITMQ_VHOST=my_vhost
    </pre>
   
    ****Kafka consumer (for listening events)****
    <pre>
    KAFKA_BROKER=kafka_broker
    KAFKA_TOPIC=tracking_topic</pre>
    ****Celery broker (to perform tasks)****
    <pre>
    CELERY_BROKER_URL=amqp://myuser:mypassword@rabbitmq:5672/my_vhost
    CELERY_RESULT_BACKEND=rpc://

    CHAT_BROKER_URL=redis://redis:6379/1</pre>


2. **Create a superuser (optional):**

You can create one manually via shell:

```
docker-compose exec web python manage.py shell
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

3. Access services:

The application will be available at: http://localhost:8000

RabbitMQ Web UI: http://localhost:15672

```
Login: my_user
Password: my_password
```

Flower (Celery monitoring): http://localhost:5555

Uploaded media (e.g. images via ImageField) will be stored in a Docker volume (media_data), mapped to /app/media/ inside the container.

