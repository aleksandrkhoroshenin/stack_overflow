from django.shortcuts import render
from .models import Question, Profile
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import Http404

def post_list(request):
    posts=Question.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'web/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Question, pk=pk)
    return render(request, 'web/post_detail.html', {'post': post})

#@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'web/post_edit.html', {'form': form})

#@login_required
def post_edit(request, pk):
    post = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'web/post_edit.html', {'form': form})

def login(request):
    return render(request, "registration/login.html", {})

def logout_view(request):
    if not request.user.is_authenticated:
        raise Http404
    logout(request)
    return redirect("login")

def login_confirm(request):

    login = request.POST['login']
    password = request.POST['password']
    user = auth.authenticate(username=login, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return redirect("post_list")

    else:
        redirect("login")

def sign_up(request):
    return render(request, 'registration/sign_up.html')


def sign_up_confirm(request):
    user = User.objects.create_user(username=request.POST['login'],
                                    email=request.POST['email'],
                                    password=request.POST['password'])

    profile = Profile(user=user)
    profile.save()
    user.save()
    auth.login(request, user)

    return redirect("post_list")

