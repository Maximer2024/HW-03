from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post, Subscriber, Category
from .filters import PostFilter
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required


class NewsListView(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    ordering = ['-time_created']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        context['paginator'] = paginator
        return context

class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'

def search(request):
    f = PostFilter(request.GET, queryset=Post.objects.all())
    return render(request, 'news/news_search.html', {'filter': f})

class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news/news_confirm_delete.html'
    success_url = '/news/'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']

class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/news_form.html'
    form_class = PostForm
    success_url = '/news/'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)

class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'news/news_form.html'
    form_class = PostForm
    success_url = '/news/'
    permission_required = ('news.change_post',)

class ArticleCreateView(CreateView):
    model = Post
    template_name = 'articles/article_form.html'
    form_class = PostForm
    success_url = '/articles/'

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def subscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subscriber, created = Subscriber.objects.get_or_create(user=request.user, category=category)
    if not created:
        subscriber.delete()
    return redirect('subscriptions')

@login_required
def subscriptions_view(request):
    subscriptions = Subscriber.objects.filter(user=request.user)
    categories = Category.objects.all()
    return render(request, 'news/subscriptions.html', {
        'subscriptions': subscriptions,
        'categories': categories,
    })