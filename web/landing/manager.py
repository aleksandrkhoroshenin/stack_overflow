from django.db import models
from django.contrib.auth.models import UserManager
from django.db.models import Sum, Count

class QuestionManager(models.Manager):

    def get_hot(self):
        return self.all().order_by('-likes')

    def get_new(self):
        return self.all().order_by('-created_date')


class CommentManager(models.Manager):

    def get_for_comment(self, question_id):
        return self.all().filter(question_id=question_id).order_by('created_date').reverse()

    # def get_hot_for_comment(self, question_id):
    #     return self.all().filter(question_id=question_id).order_by('rating').reverse()

    # def get_all_hot(self):
        # return self.all().order_by('rating').reverse()


class TagManager(models.Manager):

    def get_by_tag(self, tag_name):
        return self.filter(name=tag_name).first()

    # def hottest(self):
    #     return self.annotate(question_count=Count('question')).order_by('-question_count')
