from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from dz3.models import Profile, Question, Answer, Tag, QuestionLike,AnswerLike  # Импортируйте ваши модели
import random

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The ratio for filling the database')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        users = [
            Profile(username=get_random_string(8),
                    email=f'user{_}@example.com',
                    user_img=f'uploads/author.jpg'
                    ) for _ in range(ratio)
        ]
        Profile.objects.bulk_create(users)

        questions = [
            Question(
                question=get_random_string(12),
                description=get_random_string(50),
                author=random.choice(users)

            ) for _ in range(ratio * 10)
        ]
        Question.objects.bulk_create(questions)

        answers = [
            Answer(
                text=get_random_string(30),
                question=random.choice(questions),
                author=random.choice(users)
            ) for _ in range(ratio * 100)
        ]
        Answer.objects.bulk_create(answers)

        tags = [
            Tag(name=get_random_string(5)) for _ in range(ratio)
        ]
        Tag.objects.bulk_create(tags)

        qlikes = [
            QuestionLike(
                user=random.choice(users),
                question=random.choice(questions)
            ) for _ in range(ratio * 200)
        ]
        QuestionLike.objects.bulk_create(qlikes)
        alikes = [
            AnswerLike(
                user=random.choice(users),
                question=random.choice(questions)
            ) for _ in range(ratio * 200)
        ]
        QuestionLike.objects.bulk_create(alikes)

        self.stdout.write(self.style.SUCCESS('Успешное добавление в БД!'))
