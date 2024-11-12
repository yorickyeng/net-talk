import time

from django.core.management.base import BaseCommand
from app.models import User, Question, Answer, Tag, QuestionLike, AnswerLike


class Command(BaseCommand):
    help = 'Delete all generated data'

    def handle(self, *args, **options):
        start_time = time.time()

        # Delete Answer Likes
        answer_likes_count = AnswerLike.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {answer_likes_count} answer likes'))

        # Delete Question Likes
        question_likes_count = QuestionLike.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {question_likes_count} question likes'))

        # Delete Tags
        tags_count = Tag.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {tags_count} tags'))

        # Delete Answers
        answers_count = Answer.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {answers_count} answers'))

        # Delete Questions
        questions_count = Question.objects.all().delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {questions_count} questions'))

        # Delete Users except admin
        users_count = User.objects.exclude(is_superuser=True).delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {users_count} users'))

        end_time = time.time()
        elapsed_time = end_time - start_time
        self.stdout.write(self.style.SUCCESS(f'Command executed in {elapsed_time:.2f} seconds'))
