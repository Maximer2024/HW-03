from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django.core.management import call_command

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        call_command,
        args=['send_weekly_articles'],
        trigger=CronTrigger(day_of_week='fri', hour=18, minute=0),
        id='send_weekly_articles',
        replace_existing=True,
    )

    scheduler.start()