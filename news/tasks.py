from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime, timedelta
from news.models import Post, Subscriber


@shared_task
def send_news_notification(news_title, news_url, subscriber_emails):
    """
    Отправка уведомления о новой новости подписчикам.
    """
    subject = f'Новая новость: {news_title}'
    message = f'Прочитайте новость по ссылке: {news_url}'
    send_mail(subject, message, 'your_email@example.com', subscriber_emails)


@shared_task
def send_weekly_newsletter():
    """
    Еженедельная рассылка новостей за последние 7 дней.
    """
    one_week_ago = datetime.now() - timedelta(days=7)
    news_list = Post.objects.filter(time_created__gte=one_week_ago, post_type='NW')  # Фильтруем новости
    subscribers = Subscriber.objects.all()  # Получаем всех подписчиков

    for subscriber in subscribers:
        news_links = "\n".join(
            [f"{news.title}: {news.get_absolute_url()}" for news in news_list]
        )
        if news_links:  # Отправляем только если есть новости
            send_mail(
                'Еженедельная рассылка новостей',
                f'Вот последние новости за неделю:\n{news_links}',
                'your_email@example.com',
                [subscriber.user.email],  # Email через связь с User
            )