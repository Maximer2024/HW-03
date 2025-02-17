from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

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

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 or password in ['qwerty123', '12345678', 'password']:
            raise ValidationError('Пароль должен содержать минимум 8 символов и не может быть простым.')
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
