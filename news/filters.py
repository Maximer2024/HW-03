import django_filters
from .models import Post
from django import forms

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название')
    category = django_filters.ChoiceFilter(choices=[('tech', 'Технологии'), ('politics', 'Политика')], label='Категория')
    date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', widget=forms.DateInput(attrs={'type': 'date'}), label='Дата после')

    class Meta:
        model = Post
        fields = ['title', 'category', 'date']
