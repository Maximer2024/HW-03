from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Author, Post, Subscriber
from .tasks import send_news_notification


@receiver(post_save, sender=User)
def create_author_for_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        Author.objects.create(user=instance)


@receiver(post_save, sender=Post)
def notify_subscribers_on_news_creation(sender, instance, created, **kwargs):
    if created and instance.post_type == 'NW':
        subscribers = Subscriber.objects.filter(
            category__in=instance.categories.all()
        )
        subscriber_emails = subscribers.values_list('user__email', flat=True)

        send_news_notification.delay(
            instance.title,
            instance.get_absolute_url(),
            list(subscriber_emails),
        )