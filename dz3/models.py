from django.contrib.auth.models import User
from django.db import models

class QuestionManager(models.Manager):
    def best_questions(self):
        return self.annotate(like_count=models.Count('likes')).order_by('-like_count')
    def new_questions(self):
        return self.order_by('-created_at')
class QuestionLike(models.Model):
    STATUS_CHOICES = {
        'Disliked': -1,
        'None': 0,
        'Liked': 1,
    }
    mark = models.IntegerField(STATUS_CHOICES)
    profile = models.ForeignKey('Profile',default=0, on_delete=models.CASCADE)
    class Meta:
        unique_together = [
            ("mark", "profile"),
        ]
class AnswerLike(models.Model):
    STATUS_CHOICES = {
        'Disliked':-1,
        'None':0,
        'Liked':1,
    }
    mark = models.IntegerField(STATUS_CHOICES)
    profile = models.ForeignKey('Profile',default=0, on_delete=models.CASCADE)
    class Meta:
        unique_together = [
            ("mark", "profile"),
        ]
class Answer(models.Model):
    text = models.TextField(max_length=512)
    correct = models.BooleanField(default=False)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    likes = models.ManyToManyField(AnswerLike)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.author,self.text
class Question(models.Model):
    question = models.TextField(max_length=128)
    description = models.TextField(max_length=512)
    answers = models.ManyToManyField(Answer, related_name='answers')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    likes = models.ManyToManyField(QuestionLike)
    tags = models.ManyToManyField('Tag')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()
    def __str__(self):
        return self.question, self.author
class Tag(models.Model):
    STATUS_CHOICES = {
        'btn-primary':'blue',
        'btn-secondary':'grey',
        'btn-success':'green',
        'btn-warning':'yellow',
        'btn-danger':'red',
        'btn-info':'light-blue',
        'btn-light':'white',
        'btn-dark':'black',
    }
    name = models.CharField(max_length=16)
    theme = models.CharField(STATUS_CHOICES)
    def __str__(self):
        return self.name
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_img = models.ImageField(upload_to='uploads',null=True, blank=True)
    email = models.EmailField(null=True,blank=True)
    questions = models.ManyToManyField(Question, blank=True)
    question_likes = models.ManyToManyField(QuestionLike, blank=True,default=0, related_name='question_likes')
    answers = models.ManyToManyField(Answer, blank=True)
    answer_likes = models.ManyToManyField(AnswerLike, blank=True,default=0, related_name='answer_likes')

