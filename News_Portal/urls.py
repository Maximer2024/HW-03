from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from news.views import register, subscriptions_view
from django.conf.urls.i18n import i18n_patterns

def redirect_to_news(request):
    return redirect('/news/')

urlpatterns = [
    path('set_language/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', redirect_to_news, name='home'),
    path('news/', include('news.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('register/', register, name='register'),
    path('subscriptions/', subscriptions_view, name='subscriptions'),
)
