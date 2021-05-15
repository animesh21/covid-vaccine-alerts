from celery import Celery
from celery.schedules import crontab

from main import send_alerts

app = Celery('tasks')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls run_alerts() every 5 minutes.
    sender.add_periodic_task(crontab(minute='*/5'), run_alerts.s(), name='send vaccination alerts')


@app.task
def run_alerts():
    send_alerts()
