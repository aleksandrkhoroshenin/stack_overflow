from django.contrib import admin
from .models import Question, Comment, User

admin.site.register(Question)
admin.site.register(Comment)
