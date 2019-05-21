from django.shortcuts import render
from .models import Question, Tag, Comment
from .forms import CommentForm, LoginForm, UserSettingsForm
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .forms import QuestionForm, UserRegistrationForm, LoginForm
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login, logout

def post_list(request):
    posts = Question.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'web/post_list.html', {
        'posts': paginate(request, posts),
        'tags': paginate(request, Tag.objects.all()),
        'users':paginate(request, User.objects.all()),
        'objects': paginate(request, posts),
    })

def post_detail(request, pk):
    post = get_object_or_404(Question, pk=pk)
    return render(request, 'web/post_detail.html', {'post': post})

#@login_required
def post_new(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            # question.title = ''
            # question.make_tags(request)
            question.published_date = timezone.now()
            question.save()
            return redirect('post_detail', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'web/post_edit.html', {'form': form})

#@login_required
def post_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            # question.make_tags(request)
            question.published_date = timezone.now()
            question.save()
            return redirect('post_detail', pk=question.pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'web/post_edit.html', {'form': form})

def edit(request):
    user = get_object_or_404(User, username=request.user)

    if request.method == 'POST':
        form = UserSettingsForm(instance=user,
                               data=request.POST,
                               files=request.FILES
                              )
        if form.is_valid():
            form.save()
            return profile(request, user.id)
    else:
        form = UserSettingsForm(instance=user)

    return render(request, 'question/edit.html', {
            'form': form,
            'tags' : paginate(request, Tag.objects.hottest()),
            'users' : paginate(request, User.objects.by_rating()),
        })

def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("post_list")
    else:
        form = LoginForm()
        # logout(request)
    return render(request, 'registration/login.html', {
            'form': form
            # 'tags' : paginate(request, Tag.objects.hottest()),
            # 'users' : paginate(request, User.objects.by_rating()),
        })

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect("post_list")
    else:
        form = UserRegistrationForm()
        logout(request)
    return render(request, 'registration/sign_up.html', {
            'form': form,
            # 'tags' : paginate(request, Tag.objects.hottest()),
            # 'users' : paginate(request, User.objects.by_rating()),
        })

def signout(request):
    if not request.user.is_authenticated:
        raise Http404
    logout(request)
    #return redirect(request.GET['from'])
    return redirect("signin")


def tag(request, id):
    return render(request, 'web/sidebar.html', {
            # 'questions': paginate(request, Question.objects.get_by_tag(tag_id=id)),
            'tags': paginate(request, Tag.objects.all()),
            'users': paginate(request, User.objects.all()),
    })

def profile(request, id):
    return render(request, 'registration/user.html', {
            #'user': get_object_or_404(User, pk=id),
            'profile': get_object_or_404(User, pk=id),
            # 'tags' : paginate(request, Tag.objects.all()),
            # 'users' : paginate(request, User.objects.all()),
    })

def paginate(request, objects_list):
    paginator = Paginator(objects_list, 5)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return objects

def add_comment_to_post(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.save()
            return redirect('post_detail', pk=question.pk)
    else:
        form = CommentForm()
    return render(request, 'web/add_comment.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.question.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.question.pk)

def top(request):
    return render(request, 'web/post_list.html', {
            'posts': paginate(request, Question.objects.get_hot()),
            'tags': paginate(request, Tag.objects.all()),
            'users': paginate(request, User.objects.all()),
            'objects': paginate(request, Question.objects.all()),
        })

def new(request):
    return render(request, 'web/post_list.html', {
            'posts': paginate(request, Question.objects.get_new()),
            'tags': paginate(request, Tag.objects.all()),
            'users': paginate(request, User.objects.all()),
            'objects': paginate(request, Question.objects.all()),
        })

