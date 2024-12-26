from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.crypto import get_random_string
from dz4.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
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
                    email=f'user_{i}@example.com',
                )
                for i in range(ratio)
            ]
            for user in users:
                user.set_password('12345')
            User.objects.bulk_create(users)
            users = User.objects.all()

            self.stdout.write('Создаю профили...')
            profiles_to_create = [
                Profile(user=user,
                        nickname="Молодец_5",
                        user_img=random.choice(['author.jpg','serega2.jpg','serega3.jpg','serega4.jpg','serega5.jpg']))
                for user in users if not Profile.objects.filter(user=user).exists()
            ]
            Profile.objects.bulk_create(profiles_to_create)

            self.stdout.write('Создаю теги...')
            tags = [
                Tag(name=random.choice([
                    "Python", "Django", "Flask", "Machine Learning", "Data Science", "Web Development",
    "AI", "Deep Learning", "Data Analysis", "Automation",
    "API", "RESTful", "Tornado", "SQL", "NumPy", "Pandas", "TensorFlow", "Keras",
    "PyTorch", "Scrapy", "PyGame", "Jupyter", "Selenium", "NLP", "OpenCV", "Data Visualization"
                ]),
                    theme=random.choice([
                        'btn-primary',
                        'btn-secondary',
                        'btn-success',
                        'btn-warning',
                        'btn-danger',
                        'btn-info',
                        'btn-light',
                        'btn-dark',
                    ])) for _ in range(ratio)]
            Tag.objects.bulk_create(tags)
            tags = list(Tag.objects.all())

            self.stdout.write('Создаю вопросы...')
            profiles = list(Profile.objects.all())
            questions = []
            for _ in range(ratio * 10):
                question = Question(
                    question='How to build moon park?',
                    description='After reading Hidden Features and Dark Corners of C++/STL on comp.lang.c++.moderated, I was completely surprised that the following snippet compiled and worked in both Visual Studio 2008 and G++ 4.4. I would assume this is also valid C since it works in GCC as well.',
                    author=random.choice(profiles),
                    created_at=timezone.now(),
                )
                questions.append(question)
            Question.objects.bulk_create(questions)
            self.stdout.write('Присваиваем тэги...')
            question_tags = []

            for question in questions:
                random_tags = random.sample(tags, k=min(len(tags), 3))
                for tag in random_tags:
                    question_tags.append(Question.tags.through(question_id=question.id, tag_id=tag.id))
            Question.tags.through.objects.bulk_create(question_tags)

            self.stdout.write('Создаю ответы...')
            answers = [
                Answer(
                    text='--> is not an operator. It is in fact two separate operators, -- and >.',
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
                profile = random.choice(profiles)
                question = random.choice(questions)

                if (profile.id, question.id) not in existing_combinations:
                    q_likes.append(
                        QuestionLike(
                            mark=random.choice([-1, 0, 1]),
                            profile=profile,
                            question=question,
                        )
                    )
                    existing_combinations.add((profile.id, question.id))
            QuestionLike.objects.bulk_create(q_likes)

            self.stdout.write('Создаю лайки на ответы...')
            a_likes = []
            existing_combinations = set(
                AnswerLike.objects.values_list('profile_id', 'answer_id')
            )

            for _ in range(ratio * 200):
                profile = random.choice(profiles)
                answer = random.choice(answers)

                if (profile.id, answer.id) not in existing_combinations:
                    a_likes.append(
                        AnswerLike(
                            mark=random.choice([-1, 0, 1]),
                            profile=profile,
                            answer=answer,
                        )
                    )
                    existing_combinations.add((profile.id, answer.id))
            AnswerLike.objects.bulk_create(a_likes)
            self.stdout.write(self.style.SUCCESS('База данных успешно заполненна!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при заполнении базы данных: {e}'))
