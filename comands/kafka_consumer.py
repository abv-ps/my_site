# kafka_consumer.py у корені проєкту Django
import asyncio
import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_site.settings")
django.setup()

from aiokafka import AIOKafkaConsumer
from library.models import AuthorBookAction

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "author-book-events")


async def consume():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        group_id="django-consumer-group",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        key_deserializer=lambda k: k.decode("utf-8") if k else None,
        auto_offset_reset="earliest",
        enable_auto_commit=True
    )

    await consumer.start()
    print("Kafka consumer started and listening for events...")

    try:
        async for msg in consumer:
            key = msg.key
            value = msg.value

            print(f"[Kafka] Event key: {key} | Payload: {value}")

            action = key
            author_id = value.get("author_id")
            book_id = value.get("book_id")

            AuthorBookAction.objects.create(
                author_id=author_id,
                book_id=book_id,
                action=action
            )
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
