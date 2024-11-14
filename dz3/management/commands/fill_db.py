from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from dz3.models import Profile, Question, Answer, Tag, QuestionLike
import random

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The ratio for filling the database')

    def handle(self, *args, **options):
        ratio = options['ratio']

        users = []
        for _ in range(ratio):
            user = Profile.objects.create(username=get_random_string(8), email=f'user{_}@example.com')
            users.append(user)

        questions = []
        for _ in range(ratio * 10):
            question = Question.objects.create(
                question=get_random_string(12),
                description=get_random_string(50),
                author=random.choice(users)
            )
            questions.append(question)

        answers = []
        for _ in range(ratio * 100):
            answer = Answer.objects.create(
                content=get_random_string(30),
                question=random.choice(questions),
                author=random.choice(users)
            )
            answers.append(answer)

        tags = []
        for _ in range(ratio):
            tag = Tag.objects.create(name=get_random_string(5))
            tags.append(tag)

        likes = []
        for _ in range(ratio * 200):
            like = QuestionLike.objects.create(
                user=random.choice(users),
                question=random.choice(questions)
            )
            likes.append(like)

        self.stdout.write(self.style.SUCCESS('Успешно добавленно в БД!'))
