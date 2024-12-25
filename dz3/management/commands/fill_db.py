from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.crypto import get_random_string
from dz3.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
import random

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Multiplier for data volume.')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        if ratio <= 0:
            self.stdout.write(self.style.ERROR('Ratio должен быть > 0'))
            return
        self.stdout.write(self.style.SUCCESS(f'Заполняю бд с ratio={ratio}...'))

        try:
            self.stdout.write('Создаю пользователей...')
            users = [
                User(
                    username=f'user_{i}_{get_random_string(5)}',
                    email=f'user_{i}@example.com'
                )
                for i in range(ratio)
            ]
            User.objects.bulk_create(users)
            users = User.objects.all()

            self.stdout.write('Создаю профили...')
            profiles_to_create = [
                Profile(user=user, email=f'{user.username}@example.com', user_img='author.jpg')
                for user in users if not Profile.objects.filter(user=user).exists()
            ]
            Profile.objects.bulk_create(profiles_to_create)

            self.stdout.write('Создаю теги...')
            tags = [Tag(name=get_random_string(5)) for _ in range(ratio)]
            Tag.objects.bulk_create(tags)
            tags = list(Tag.objects.all())

            self.stdout.write('Создаю вопросы...')
            profiles = list(Profile.objects.all())
            questions = []
            for _ in range(ratio * 10):
                question = Question(
                    question=get_random_string(20),
                    description=get_random_string(50),
                    author=random.choice(profiles),
                    created_at=timezone.now(),
                )
                question.save()  # Сохраняем вопрос перед добавлением тегов
                question.tags.set(random.sample(tags, k=min(len(tags), 5)))  # Присваиваем случайные теги
                questions.append(question)

            self.stdout.write('Создаю ответы...')
            answers = [
                Answer(
                    text=get_random_string(30),
                    question=random.choice(questions),
                    author=random.choice(profiles),
                ) for _ in range(ratio * 100)
            ]
            Answer.objects.bulk_create(answers)
            answers = list(Answer.objects.all())

            self.stdout.write('Создаю лайки на вопросы...')
            q_likes = []
            existing_combinations = set(
                QuestionLike.objects.values_list('profile_id', 'question_id')
            )

            for _ in range(ratio * 200):
                profile = random.choice(profiles)  # Случайный профиль
                question = random.choice(questions)  # Случайный вопрос

                # Проверяем, существует ли такая комбинация в базе
                if (profile.id, question.id) not in existing_combinations:
                    q_likes.append(
                        QuestionLike(
                            mark=random.choice([-1, 0, 1]),
                            profile=profile,
                            question=question,
                        )
                    )
                    existing_combinations.add((profile.id, question.id))  # Добавляем в набор существующих комбинаций
            QuestionLike.objects.bulk_create(q_likes)

            self.stdout.write('Создаю лайки на ответы...')
            a_likes = []
            existing_combinations = set(
                AnswerLike.objects.values_list('profile_id', 'answer_id')
            )

            for _ in range(ratio * 200):
                profile = random.choice(profiles)
                answer = random.choice(answers)

                # Проверяем, существует ли такая комбинация в базе
                if (profile.id, answer.id) not in existing_combinations:
                    a_likes.append(
                        AnswerLike(
                            mark=random.choice([-1, 0, 1]),
                            profile=profile,
                            answer=answer,
                        )
                    )
                    existing_combinations.add((profile.id, answer.id))  # Добавляем в набор существующих комбинаций
            AnswerLike.objects.bulk_create(a_likes)
            self.stdout.write(self.style.SUCCESS('База данных успешно заполненна!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при заполнении базы данных: {e}'))
