from celery import shared_task
import logging
logger = logging.getLogger(__name__)


@shared_task
def add(x, y):
    return x + y

@shared_task
def generate(prompt):
    logger.info(prompt)


@shared_task
def log_message_task():
    logger.info('This is a log message from the Celery task.')