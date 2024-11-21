from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from myapp.models import Subscriber, Post

class Command(BaseCommand):
    help = 'Send weekly article list to subscribers'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        last_week = now - timezone.timedelta(days=7)
        subscribers = Subscriber.objects.all()

        for subscriber in subscribers:
            new_posts = Post.objects.filter(categories=subscriber.category, time_created__gte=last_week)
            if new_posts.exists():
                article_links = "\n".join([f"{post.title}: http://127.0.0.1:8000/news/{post.id}/" for post in new_posts])
                send_mail(
                    'Еженедельные статьи',
                    f'Новые статьи за последнюю неделю:\n{article_links}',
                    'from@example.com',
                    [subscriber.user.email],
                    fail_silently=False,
                )
