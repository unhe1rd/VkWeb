from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

# Create your views here.


def paginate(objects, request, per_page):

    paginator = Paginator(objects, per_page)
    page = request.GET.get('page', 1)
    try:
        page_items = paginator.page(page).object_list
    except PageNotAnInteger:
        page_items = paginator.page(1).object_list
    except EmptyPage:
        raise Http404("Страница не существует")
    return page_items


def index(request):
    questions = [
        {
            'id': i,
            'title': f'Question {i}',
            'content': f'How to feed a cat {i}'
        } for i in range(100)
    ]
    return render(request, 'index.html', context={'questions': paginate(questions, request, per_page=5)})


def tag(request, tag_name):
    questions = [
        {
            'id': i,
            'title': f'Question {i}',
            'content': f'How to feed a cat {i}'
        } for i in range(100)
    ]
    tag = {
        'tag': tag_name
    }
    return render(request, 'tag.html', context={'questions': paginate(questions, request, per_page=5), 'tag': tag})


def hot(request):
    questions = [
        {
            'id': i,
            'title': f'Question {i}',
            'content': f'How to feed a cat {i}'
        } for i in range(100)
    ]
    return render(request, 'index.html', context={'questions': paginate(questions, request, per_page=5)})


def question(request, question_id):
    questions = [
        {
            'id': i,
            'title': f'Question {i}',
            'content': f'How to feed a cat {i}'
        } for i in range(100)
    ]
    main = questions[question_id]
    return render(request, 'question.html', {'questions': questions, 'main': main})


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def settings(request):
    return render(request, 'settings.html')


