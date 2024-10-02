from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class NewsListView(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    ordering = ['-time_created']

class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'