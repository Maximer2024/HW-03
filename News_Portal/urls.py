from django.contrib import admin
from django.urls import path, include
from news import views
from news.views import NewsListView, NewsDetailView, NewsCreateView, NewsUpdateView, NewsDeleteView, ArticleCreateView, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register')
]
