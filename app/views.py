from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from app.models import Question, Tag, Answer, get_random_users, get_popular_tags
from app.utils import paginate


def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, '404.html', {'user': user})  # На будущее


def get_common_context(request):
    random_users = get_random_users()
    popular_tags = get_popular_tags()
    tags = Tag.objects.all()
    return {
        'random_users': random_users,
        'popular_tags': popular_tags,
        'tags': tags
    }


def index(request):
    questions = Question.objects.new()
    page = paginate(questions, request)

    context = get_common_context(request)
    context.update({
        'questions': page.object_list,
        'page_obj': page,
        'custom_title': 'New Questions'
    })
    return render(request, 'index.html', context)


def hot(request):
    questions = Question.objects.hot()
    page = paginate(questions, request)

    context = get_common_context(request)
    context.update({
        'questions': page.object_list,
        'page_obj': page,
        'custom_title': 'Hot Questions'
    })
    return render(request, 'hot.html', context)


def question(request, question_id):
    question_obj = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question_obj)
    tags = question_obj.tags.all()

    page = paginate(answers, request)

    context = get_common_context(request)
    context.update({
        'question': question_obj,
        'answers': page.object_list,
        'page_obj': page,
        'tags': tags,
        'custom_title': f'Question {question_id}'
    })
    return render(request, 'question.html', context)


def tag(request, tag_name):
    tag_obj = get_object_or_404(Tag, name=tag_name)
    questions = tag_obj.question.all()
    page = paginate(questions, request)

    context = get_common_context(request)
    context.update({
        'tag_name': tag_name,
        'questions': page.object_list,
        'page_obj': page,
        'custom_title': f'Tag: {tag_name}'
    })
    return render(request, 'tag.html', context)


def login(request):
    context = get_common_context(request)
    context.update({'custom_title': 'Login'})
    return render(request, 'login.html', context)


def signup(request):
    context = get_common_context(request)
    context.update({'custom_title': 'Signup'})
    return render(request, 'signup.html', context)


def settings(request):
    context = get_common_context(request)
    context.update({'custom_title': 'Settings'})
    return render(request, 'settings.html', context)


def ask(request):
    context = get_common_context(request)
    context.update({'custom_title': 'New Question'})
    return render(request, 'ask.html', context)
