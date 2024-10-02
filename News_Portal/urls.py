from django.contrib import admin
from django.urls import path
from news import views
from news.views import NewsListView, NewsDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
]
