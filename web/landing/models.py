# from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from landing.manager import *


class ModelManager(models.Manager):
    def new(self):
        return self.order_by('-date')

    def hot(self):
        return self.order_by('-likes')

    def get_by_tag(self, tag_id):
        return self.all().filter(tags__id=tag_id)

    def hottest(self):
        return self.annotate(question_count=Count('question')).order_by('-question_count')


# class User(AbstractUser):
#     User = settings.AUTH_USER_MODEL
#     upload = models.ImageField(upload_to='uploads/%Y/%m/%d/')
#     # registration_date = models.DateTimeField(default=timezone.now, verbose_name="Дата решистрации")
#     # rating = models.IntegerField(default=0, verbose_name="Рейтинг пользователя")
#     # author = models.ForeignKey(
#     #     settings.AUTH_USER_MODEL,
#     #     on_delete=models.CASCADE,
#     # )
#     def __str__(self):
#         return self.username


class Tag(models.Model):
    title = models.CharField(max_length=120, verbose_name=u"Заголовок ярлыка")

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    upload = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    # nickname = models.TextField()
    # avatar = models.ImageField(default='')

    def __str__(self):
        return self.user.username

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    likes = models.IntegerField(blank=True, null=True)
    dislikes = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    objects = QuestionManager()

    def like(self):
        self.likes += 1
        self.save()

    def dislike(self):
        self.dislikes += 1
        self.save()

    def make_tags(self, request):
        tags = request.POST["question_tags"].split(", ")

        for tag in tags:
            try:
                current_tag = Tag.objects.get(name=tag)

            except:
                current_tag = Tag(name=tag)
                current_tag.save()
            self.save()
            current_tag.question.add(self)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
