from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from news import views
from news.views import NewsListView, NewsDetailView, NewsCreateView, NewsUpdateView, NewsDeleteView, ArticleCreateView, register, subscriptions_view
from django.conf.urls.i18n import set_language


def redirect_to_news(request):
    return redirect('/news/')

urlpatterns = [
    path('set_language/', set_language, name='set_language'),
    path('admin/', admin.site.urls),
    path('', redirect_to_news),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('accounts/', include('allauth.urls')),
    path('subscriptions/', subscriptions_view, name='subscriptions'),
]
