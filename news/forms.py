from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Электронная почта")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4:
            raise ValidationError('Логин должен содержать минимум 4 символа.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not (email.endswith('@mail.ru') or email.endswith('@gmail.com') or email.endswith('@yandex.ru')):
            raise ValidationError('Электронная почта должна быть @mail.ru, @gmail.com или @yandex.ru.')
        return email
