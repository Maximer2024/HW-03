from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
import logging
from .models import Post, Subscriber, Category
from .forms import RegistrationForm
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    ordering = ['-time_created']
    paginate_by = 10

class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'

class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.delete_post',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories']

class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'articles/article_form.html'
    form_class = PostForm
    success_url = reverse_lazy('news_list')
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Создание статьи"
        return context

class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/news_form.html'
    form_class = PostForm
    success_url = reverse_lazy('news_list')
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)

class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'news/news_form.html'
    form_class = PostForm
    success_url = reverse_lazy('news_list')
    permission_required = ('news.change_post',)

@csrf_exempt
def delete_news(request, pk):

    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        logger.warning("Попытка удалить новость не через AJAX")
        return JsonResponse({"success": False, "error": "Запрос должен быть AJAX"}, status=400)

    if not request.user.is_authenticated:
        logger.warning("Попытка удалить новость неавторизованным пользователем")
        return JsonResponse({"success": False, "error": "Вы не авторизованы!"}, status=401)

    if not request.user.is_superuser:
        logger.warning("Попытка удалить новость пользователем без прав")
        return JsonResponse({"success": False, "error": "Недостаточно прав!"}, status=403)

    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        password = request.POST.get("password")

        if not request.user.check_password(password):
            logger.warning(f"Неверный пароль при удалении новости {pk}")
            return JsonResponse({"success": False, "error": "Неверный пароль!"}, status=400)

        post.delete()
        logger.info(f"Новость {pk} удалена пользователем {request.user.username}")
        return JsonResponse({"success": True})

    logger.error("Удаление вызвано с неправильным методом запроса")
    return JsonResponse({"success": False, "error": "Неверный метод!"}, status=405)

@login_required
@user_passes_test(is_superuser)
def admin_panel(request):
    posts = Post.objects.all()
    messages.info(request, "Добро пожаловать в админ-панель!")
    return render(request, 'news/admin_panel.html', {'posts': posts})

@login_required
def subscriptions_view(request):
    subscriptions = Subscriber.objects.filter(user=request.user)
    categories = Category.objects.all()
    return render(request, 'news/subscriptions.html', {
        'subscriptions': subscriptions,
        'categories': categories,
    })

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно! Теперь войдите в систему.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
