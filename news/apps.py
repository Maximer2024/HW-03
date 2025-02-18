from django.apps import AppConfig
from apscheduler.triggers.cron import CronTrigger
from django.core.management import call_command

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals
        import news.translation
        from news.scheduler import start_scheduler

        start_scheduler()
