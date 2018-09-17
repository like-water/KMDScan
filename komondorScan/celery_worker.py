# -*- coding: utf-8 -*-
from app import create_app, celery

app = create_app()
app.app_context().push()

# celery worker -A celery_worker.celery -l INFO
