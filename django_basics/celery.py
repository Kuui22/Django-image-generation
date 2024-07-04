import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_basics.settings')

app = Celery('django_basics')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    broker_url='memory://',  # Use in-memory broker for synchronous execution
    task_always_eager=True,  # Execute tasks locally instead of sending them to a worker
    task_eager_propagates=True,  # Ensure exceptions propagate
    worker_pool='solo'  # Use solo pool for synchronous execution
)
# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')