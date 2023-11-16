from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.http import Http404
from .models import Question, Answer, Tag, Profile
from django.db.models import Count

# Create your views here.


def get_best_members(Profile):
    return Profile.objects.annotate(rating=Count('user__question')).order_by('rating')[:10]


def get_tag(Tag):
    return Tag.objects.annotate(num_questions=Count('question')).order_by('-num_questions')[:9]


popular_tags = get_tag(Tag=Tag)
best_members = get_best_members(Profile=Profile)

def paginate(objects, request, per_page):
    paginator = Paginator(objects, per_page)
    page = int(request.GET.get('page', 1))
    try:
        page_items = paginator.page(page).object_list
    except PageNotAnInteger:
        page_items = paginator.page(1).object_list
    except EmptyPage:
        raise Http404('Страница не найдена')
    return page_items


def index(request):
    questions = Question.objects.sorted_by_created_at()
    return render(request, 'index.html', context={'questions': paginate(questions, request, per_page=5), 'popular_tags': popular_tags, 'best_members': best_members})


def tag(request, tag_name):
    questions = Question.objects.filter_by_tag(tag_name)
    tag = {'tag': tag_name}
    return render(request, 'tag.html', context={'questions': paginate(questions, request, per_page=5),
                                                'tag': tag, 'popular_tags': popular_tags,
                                                'best_members': best_members})


def hot(request):
    questions = Question.objects.get_hot_questions()
    return render(request, 'index.html', context={'questions': paginate(questions, request, per_page=5),'popular_tags': popular_tags, 'best_members': best_members})


def question(request, question_id):
    try:
        main = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Такого вопроса не существует!')
    answers = Answer.objects.get_answers_for_question(question_id)
    return render(request, 'question.html', {'answers': paginate(answers, request, per_page=5), 'main': main, 'popular_tags': popular_tags, 'best_members': best_members})


def ask(request):
    return render(request, 'ask.html', {'popular_tags': popular_tags, 'best_members': best_members})


def login(request):
    return render(request, 'login.html', {'popular_tags': popular_tags, 'best_members': best_members})


def register(request):
    return render(request, 'register.html', {'popular_tags': popular_tags, 'best_members': best_members})


def settings(request):
    return render(request, 'settings.html', {'popular_tags': popular_tags, 'best_members': best_members})


def handler404(request, exception):
    return render(request, 'warning.html', status=404)


