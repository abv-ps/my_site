import asyncio
import os
import django
import json
import logging

from aiokafka.errors import KafkaConnectionError
from asgiref.sync import sync_to_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_site.settings")
django.setup()

from aiokafka import AIOKafkaConsumer
from library.models import AuthorBookAction

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "author-book-events")

logger = logging.getLogger("kafka_consumer")
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


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

    while True:
        try:
            await consumer.start()
            print("Kafka consumer started and listening for events...")
            break
        except KafkaConnectionError:
            print("Kafka not ready, retrying in 5 seconds...")
            await asyncio.sleep(5)

    try:
        async for msg in consumer:
            key = msg.key
            value = msg.value

            print(f"[Kafka] Event key: {key} | Payload: {value}")

            action = key
            author_id = value.get("author_id")
            book_id = value.get("book_id")
            try:
                await sync_to_async(AuthorBookAction.objects.create)(
                    author_id=author_id,
                    book_id=book_id,
                    action=action
                )
                logger.info(f"Saved AuthorBookAction to DB: author_id={author_id}, book_id={book_id}, action={action}")
            except Exception as e:
                logger.error(f"Failed to save AuthorBookAction: {e}")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
