from django import forms
from .models import Question, Comment
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

text_validator = RegexValidator(r"[а-яА-Яa-zA-Z]", "Текст должен содержать буквы")
tags_validator = RegexValidator(r"[а-яА-Яa-zA-Z]", "Тэги состоят из букв")
password_validator = RegexValidator(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                                   "Пароль - 8 символов. Буквы и цифры")

class PostForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)