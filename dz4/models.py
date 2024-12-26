from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils import timezone


class QuestionManager(models.Manager):
    def order_by_date(self):
        return self.get_queryset().annotate(total_marks=Sum('questionlike__mark')).order_by('-created_at')

    def order_by_mark(self):
        return self.get_queryset().annotate(total_marks=Sum('questionlike__mark')).order_by('-total_marks')
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=120, null=True, blank=True)
    user_img = models.ImageField(upload_to='uploads', null=True, blank=True)


    def __str__(self):
        return self.user.username

class Tag(models.Model):
    STATUS_CHOICES = [
        ('btn-primary', 'blue'),
        ('btn-secondary', 'grey'),
        ('btn-success', 'green'),
        ('btn-warning', 'yellow'),
        ('btn-danger', 'red'),
        ('btn-info', 'light-blue'),
        ('btn-light', 'white'),
        ('btn-dark', 'black'),
    ]
    name = models.CharField(max_length=32)
    theme = models.CharField(max_length=32, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name

class Question(models.Model):
    question = models.TextField(max_length=128)
    description = models.TextField(max_length=512)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()
    def __str__(self):
        return f"{self.question} (by {self.author})"

class Answer(models.Model):
    text = models.TextField(max_length=512)
    correct = models.BooleanField(default=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} (by {self.author})"

class QuestionLike(models.Model):
    STATUS_CHOICES = [
        (-1, 'Disliked'),
        (0, 'None'),
        (1, 'Liked'),
    ]
    mark = models.IntegerField(choices=STATUS_CHOICES)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ("profile", "question"),
        ]

class AnswerLike(models.Model):
    STATUS_CHOICES = [
        (-1, 'Disliked'),
        (0, 'None'),
        (1, 'Liked'),
    ]
    mark = models.IntegerField(choices=STATUS_CHOICES)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = [('profile', 'answer')]

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=32, label="Password")
    repeat_password = forms.CharField(widget=forms.PasswordInput, max_length=32, label="Repeat password")
    user_img = forms.ImageField(required=False, label="Upload avatar")
    nickname = forms.CharField(max_length=32, required=True, label="Nickname")
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if password != repeat_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
