# Generated by Django 4.2.16 on 2024-11-13 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=512)),
                ('correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AnswerLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(verbose_name={'Disliked': -1, 'Liked': 1, 'None': 0})),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_img', models.ImageField(blank=True, null=True, upload_to='uploads')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('answers', models.ManyToManyField(blank=True, to='dz3.answer')),
                ('answers_like', models.ManyToManyField(blank=True, to='dz3.answerlike')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(verbose_name={'Disliked': -1, 'Liked': 1, 'None': 0})),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('theme', models.CharField(verbose_name={'btn-danger': 'red', 'btn-dark': 'black', 'btn-info': 'light-blue', 'btn-light': 'white', 'btn-primary': 'blue', 'btn-secondary': 'grey', 'btn-success': 'green', 'btn-warning': 'yellow'})),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=128)),
                ('description', models.TextField(max_length=512)),
                ('answers', models.ManyToManyField(related_name='answers', to='dz3.answer')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dz3.profile')),
                ('likes', models.ManyToManyField(to='dz3.questionlike')),
                ('tags', models.ManyToManyField(to='dz3.tag')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='questions',
            field=models.ManyToManyField(blank=True, to='dz3.question'),
        ),
        migrations.AddField(
            model_name='profile',
            name='questions_like',
            field=models.ManyToManyField(blank=True, to='dz3.questionlike'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dz3.profile'),
        ),
        migrations.AddField(
            model_name='answer',
            name='likes',
            field=models.ManyToManyField(to='dz3.answerlike'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dz3.question'),
        ),
    ]
