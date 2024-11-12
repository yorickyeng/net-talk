import random

from django.contrib.auth.models import User
from django.db import models


def get_random_users(count=5):
    users = User.objects.all()
    return random.sample(list(users), count)


def get_popular_tags(count=10):
    tags = Tag.objects.all()
    return random.sample(list(tags), min(len(tags), count))


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-created_at')

    def hot(self):
        return self.annotate(like_count=models.Count('likes')).order_by('-like_count')


class TagManager(models.Manager):
    def get_popular_tags(self, count=10):
        tags = self.all()
        return random.sample(list(tags), min(len(tags), count))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='default_profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    name = models.CharField(max_length=255)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    def __str__(self):
        return self.name


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField()
    correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer


class Tag(models.Model):
    name = models.CharField(max_length=255)
    question = models.ManyToManyField(Question, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TagManager()

    def __str__(self):
        return self.name


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user.username} liked {self.question.name}"


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer')

    def __str__(self):
        return f"{self.user.username} liked {self.answer.answer}"
