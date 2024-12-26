from django.core.management.base import BaseCommand
from dz4.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            # Удаляем все объекты в моделях
            self.stdout.write('Удаляем все пользователи...')
            User.objects.all().delete()

            self.stdout.write('Удаляем все профили...')
            Profile.objects.all().delete()

            self.stdout.write('Удаляем все вопросы...')
            Question.objects.all().delete()

            self.stdout.write('Удаляем все ответы...')
            Answer.objects.all().delete()

            self.stdout.write('Удаляем все теги...')
            Tag.objects.all().delete()

            self.stdout.write('Удаляем все лайки на вопросы...')
            QuestionLike.objects.all().delete()

            self.stdout.write('Удаляем все лайки на ответы...')
            AnswerLike.objects.all().delete()

            self.stdout.write(self.style.SUCCESS('База данных успешно очищена!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при очистке базы данных: {e}'))
