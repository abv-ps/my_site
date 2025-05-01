#!/bin/bash

watchmedo auto-restart \
  --patterns=".py" \
  --recursive \
  --directory=/app \
  -- celery -A celery_tasks worker --loglevel=info --concurrency=4


#watchfiles "celery -A celery_tasks worker --loglevel=info"