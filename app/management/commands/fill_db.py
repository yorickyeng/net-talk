import time

from django.core.management.base import BaseCommand
from app.models import User, Question, Answer, Tag, QuestionLike, AnswerLike
from django.utils.crypto import get_random_string
import random


class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        start_time = time.time()
        ratio = options['ratio']

        # Generate Users
        users = [
            User(
                username=f'user_{i}_{get_random_string(5)}',
                email=f'user_{i}@example.com'
            )
            for i in range(ratio)
        ]
        User.objects.bulk_create(users, batch_size=1000)
        users = list(User.objects.all())
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(users)} users'))

        # Generate Questions
        questions = [
            Question(
                name=f'Question {i}',
                question='This is a sample question body.'
            )
            for i in range(ratio * 10)
        ]
        Question.objects.bulk_create(questions, batch_size=1000)
        questions = list(Question.objects.all())
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(questions)} questions'))

        # Generate Answers
        answers = [
            Answer(
                question=random.choice(questions),
                answer='This is a sample answer',
                correct=random.choice([True, False])
            )
            for _ in range(ratio * 100)
        ]
        Answer.objects.bulk_create(answers, batch_size=1000)
        answers = list(Answer.objects.all())  # Reload answers from the database
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(answers)} answers'))

        # Generate Tags
        tag_names = [f'tag_{i}' for i in range(ratio)]
        existing_tags = Tag.objects.filter(name__in=tag_names).values_list('name', flat=True)
        new_tags = [
            Tag(name=tag_name) for tag_name in tag_names if tag_name not in existing_tags
        ]
        Tag.objects.bulk_create(new_tags, batch_size=1000)
        tags = list(Tag.objects.filter(name__in=tag_names))
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(new_tags)} tags'))

        # Generate Tag-Question Relations
        for tag in tags:
            random_questions = random.sample(questions, random.randint(1, 5))
            tag.question.add(*random_questions)

        self.stdout.write(self.style.SUCCESS('Successfully created tag-question relations'))

        # Generate Question Likes
        question_likes = []
        liked_pairs = set()
        for _ in range(ratio * 200):
            user = random.choice(users)
            question = random.choice(questions)
            if (user.id, question.id) not in liked_pairs:
                liked_pairs.add((user.id, question.id))
                question_likes.append(QuestionLike(user=user, question=question))
        QuestionLike.objects.bulk_create(question_likes, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(question_likes)} question likes'))

        # Generate Answer Likes
        answer_likes = []
        liked_pairs = set()
        for _ in range(ratio * 200):
            user = random.choice(users)
            answer = random.choice(answers)
            if (user.id, answer.id) not in liked_pairs:
                liked_pairs.add((user.id, answer.id))
                answer_likes.append(AnswerLike(user=user, answer=answer))
        AnswerLike.objects.bulk_create(answer_likes, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(answer_likes)} answer likes'))

        end_time = time.time()
        elapsed_time = end_time - start_time
        self.stdout.write(self.style.SUCCESS(f'Command executed in {elapsed_time:.2f} seconds'))
