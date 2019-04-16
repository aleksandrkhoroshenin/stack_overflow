#from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class ModelManager(models.Manager):
    def new(self):
        return self.order_by('-date')

    def hot(self):
        return self.order_by('-likes')

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    likes = models.IntegerField(blank=True, null=True)
    dislikes = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    objects = ModelManager()

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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # nickname = models.TextField()
    # avatar = models.ImageField(default=)

    def __str__(self):
        return self.user.username

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    text = models.TextField()
    correct = models.BooleanField(default=False)
    user = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)


class Tag(models.Model):

    question = models.ManyToManyField(Question, related_name="tags", related_query_name="tag")
    name = models.TextField()

