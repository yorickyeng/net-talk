import copy

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is text for question #{i}'
    } for i in range(30)
]
TAGS = [
    {'title': 'blablabla', 'id': 1},
    {'title': 'interesting', 'id': 2},
    {'title': 'stupid', 'id': 3},
]
ANSWERS = [
    {'id': i} for i in range(3)
]


def index(request):
    page = paginate(QUESTIONS, request)
    return render(
        request, 'index.html',
        context={'questions': page.object_list, 'page_obj': page, 'tags': TAGS, 'custom_title': 'New Questions'}
    )


def hot(request):
    hot_questions = copy.deepcopy(QUESTIONS)
    hot_questions.reverse()
    page = paginate(hot_questions, request)
    return render(
        request, 'hot.html',
        context={'questions': page.object_list, 'page_obj': page, 'tags': TAGS, 'custom_title': 'Hot Questions'}
    )


def question(request, question_id):
    one_question = QUESTIONS[question_id]
    return render(
        request, 'question.html',
        context={'item': one_question, 'answers': ANSWERS, 'tags': TAGS, 'custom_title': 'Question ' + str(question_id)}
    )


def tag(request, tag_name):
    page = paginate(QUESTIONS, request)
    return render(
        request, 'tag.html',
        context={'tag_name': tag_name, 'tags': TAGS, 'questions': page.object_list, 'page_obj': page,
                 'custom_title': 'Tag: ' + str(tag_name)}
    )


def login(request):
    return render(
        request, 'login.html',
        context={'tags': TAGS, 'custom_title': 'Login'}
    )


def signup(request):
    return render(
        request, 'signup.html',
        context={'tags': TAGS, 'custom_title': 'Signup'}
    )


def settings(request):
    return render(
        request, 'settings.html',
        context={'tags': TAGS, 'custom_title': 'Settings'}
    )


def ask(request):
    return render(
        request, 'ask.html',
        context={'tags': TAGS, 'custom_title': 'New Question'}
    )


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_num = int(request.GET.get('page', 1))

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page
