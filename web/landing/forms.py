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

class QuestionForm(forms.ModelForm):

    def clean(self):
        title = self.cleaned_data.get('title')
        tags = self.cleaned_data.get('tags')
        if len(str(title)) > 100:
            raise ValidationError("Sorry, a title should contain no more than 100 characters. ")
        if len(str(tags)) > 20:
            raise ValidationError("Sorry, length of tags line must be no more than 20 characters.  ")
        return self.cleaned_data

    class Meta:
        model = Question
        fields = ('title', 'text',) # 'tags'

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)