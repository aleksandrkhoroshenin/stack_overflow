from django import forms
from .models import Question, Comment, Profile
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

text_validator = RegexValidator(r"[а-яА-Яa-zA-Z]", "Текст должен содержать буквы")
tags_validator = RegexValidator(r"[а-яА-Яa-zA-Z]", "Тэги состоят из букв")
password_validator = RegexValidator(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                                   "Пароль - 8 символов. Буквы и цифры")

class QuestionForm(forms.ModelForm):

    # tags inputField()
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
        fields = ('title', 'text') # 'tags'

    def save(self, commit=True):
        cdata = self.cleaned_data
        question = Question(**cdata)
        question.author = self.profile
        if commit:
            question.save()
        return question

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class LoginForm(forms.Form):
     username = forms.CharField(min_length=3)
     password = forms.CharField(widget=forms.PasswordInput)
     # email = forms.CharField(widget=forms.EmailInput)

     def clean(self):
         username = self.cleaned_data.get('username')
         password = self.cleaned_data.get('password')
         user = authenticate(username=username, password=password)
         if not user or not user.is_active:
             raise ValidationError("Логин или пароль неверны")
         return self.cleaned_data

     class Meta:
         model = Profile
         fields = ['username', 'password']

class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 1,
        'maxlength': 30,
        'placeholder': 'Имя'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 1,
        'maxlength': 30,
        'placeholder': 'Фамилия'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 5,
        'maxlength': 30,
        'placeholder': 'Логин'}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'E-mail'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'}))

    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтверждение пароля'}))

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_repeat")

        if password != password_confirmation:
            raise ValidationError("Password and Repeat password does not match")
        return cleaned_data

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'email', 'upload']

class UserSettingsForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 2,
        'maxlength': 30,
        'placeholder': 'Имя'}))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 2,
        'maxlength': 30,
        'placeholder': 'Фамилия'}))

    username = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 5,
        'maxlength': 30,
        'placeholder': 'Логин'}))

    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'E-mail'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'email', 'upload']

