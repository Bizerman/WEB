from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.shortcuts import render

from dz4.models import Question, Tag, Answer

top_tags = Tag.objects.annotate(question_count=Count('question')).order_by('-question_count')[:8]
def questions_sort(sort):
    if sort == None:
        return Question.objects.order_by_mark()
    else:
        return Question.objects.order_by_date()
def render_questions_list_page(request,sort = None,tag=None):
    if tag != None:
        questions = questions_sort(sort).filter(tags__name=tag)
    else:
        questions = questions_sort(sort)
    questions_with_answers_len = []
    for question in questions:
        answers_count = Answer.objects.filter(question=question).count()  # Подсчитываем количество ответов для каждого вопроса
        questions_with_answers_len.append({
            'main_attributes': question,
            'answers_len': answers_count
        })

    page = paginate(questions_with_answers_len, request, 20)
    return render(request, 'index.html', {'auth': False, 'tags':top_tags,'questions':page.object_list,'tag': tag, 'page_obj':page,})
def render_hot_questions_page(request):
    return render_questions_list_page(request,'hot')
def render_questions_with_tag_page(request, tag):
    return render_questions_list_page(request,tag=tag)
def render_ask_page(request):
    return render(request, 'ask.html', {'auth': 'Dr.Pepper', 'tags': top_tags})
def render_question_page(request,id):
    question = Question.objects.annotate(total_marks=Sum('questionlike__mark')).get(id=id)
    answers = Answer.objects.annotate(total_marks=Coalesce(Sum('answerlike__mark'), 0)).filter(question=id).order_by('-total_marks')
    page = paginate(answers, request, 30)
    return render(request, 'question.html',{'auth': 'Dr.Pepper', 'tags': top_tags, 'question':question, 'page_obj':page,})
def render_settings_page(request):
    return render(request, 'settings.html', {'auth': 'Dr.Pepper', 'tags': top_tags})
def render_login_page(request):
    return render(request, 'login.html',{'auth': False, 'tags': top_tags})
def render_signup_page(request):
    return render(request, 'signup.html',{'auth': False, 'tags': top_tags})
def logout(request):
    return render_questions_list_page(request)
def paginate(objects_list,request,per_page):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)
    try:
        return paginator.page(page_num)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        raise PageNotAnInteger("'page' должен быть целым числом.")