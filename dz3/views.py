from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.shortcuts import render

from dz3.models import Question, Tag, QuestionLike, Answer

tags = [{'name': 'python',
         'theme': 'btn-primary',
         },
        {'name': 'MySQL',
         'theme': 'btn-secondary',
         },
        {'name': 'Sberbank',
         'theme': 'btn-success',
         },
        {'name': 'Opera',
         'theme': 'btn-danger',
         },
        {'name': 'Django',
         'theme': 'btn-warning',
         },
        {'name': 'Vk',
        'theme': 'btn-info',
        },
        ]
# questions=[]
# for i in range(1,60):
#     questions.append({'id':i,
#     'question': 'How to build moon park?',
#     'text':'After reading Hidden Features and Dark Corners of C++/STL on comp.lang.c++.moderated, I was completely surprised that the following snippet compiled and worked in both Visual Studio 2008 and G++ 4.4. I would assume this is also valid C since it works in GCC as well.',
#     'answers':[{
#          'author_img':'https://avatars.mds.yandex.net/i?id=216e1ca12bc36664c50201ddff39db74_l-10932557-images-thumbs&n=13',
#          'text':'--> is not an operator. It is in fact two separate operators, -- and >.'
#                 'The code in the condition decrements x, while returning xs original (not decremented) value, and then compares the original value with 0 using the > operator.'
#                 'To better understand, the statement could be written as follows:'
#                 'while( (x--) > 0 )',
#          'correct':True,
#          'mark':5
#      },],
#     'answers_len':2,
#     'author_img':'https://steamuserimages-a.akamaihd.net/ugc/1871835125756588981/03DA856A823722D774E923087DCA4D056851920C/?imw=512&imh=512&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true',
#     'mark':5,
#     'tags':[tags[0],tags[1]],
#      })
#     for j in range(1,31):
#         question = next(question for question in questions if question['id'] == i)
#         question['answers'].append({
#          'author_img':'https://avatars.mds.yandex.net/i?id=ddbcf8d00cf711d860f1108f607be299f427c042-12994680-images-thumbs&n=13',
#          'text':'--> is an operator',
#          'correct':False,
#          'mark':0
#      })
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
    return render(request, 'index.html', {'auth': 'Dr.Pepper', 'tags':Tag.objects.all(),'questions':page.object_list,'tag': tag, 'page_obj':page,})
def render_hot_questions_page(request):
    return render_questions_list_page(request,'hot')
def render_questions_with_tag_page(request, tag):
    return render_questions_list_page(request,'hot',tag)
def render_ask_page(request):
    return render(request, 'ask.html', {'auth': 'Dr.Pepper', 'tags': Tag.objects.all()})
def render_question_page(request,id):
    question = Question.objects.annotate(total_marks=Sum('questionlike__mark')).get(id=id)
    answers = Answer.objects.annotate(total_marks=Coalesce(Sum('answerlike__mark'), 0)).filter(question=id).order_by('-total_marks')
    page = paginate(answers, request, 30)
    return render(request, 'question.html',{'auth': 'Dr.Pepper', 'tags': Tag.objects.all(), 'question':question, 'page_obj':page,})
def render_settings_page(request):
    return render(request, 'settings.html', {'auth': 'Dr.Pepper', 'tags': Tag.objects.all()})
def render_login_page(request):
    return render(request, 'login.html',{'auth': False, 'tags': Tag.objects.all()})
def render_signup_page(request):
    return render(request, 'signup.html',{'auth': False, 'tags': Tag.objects.all()})
def logout(request):
    return render(request, 'index.html', {'auth': False, 'tags':Tag.objects.all(), 'tag': None,'questions':Question.objects.all(), })
def paginate(objects_list,request,per_page):
    try:
        page_num = int(request.GET.get('page', 1))
    except ValueError:
        raise PageNotAnInteger("'page' должен быть целым числом.")
    paginator = Paginator(objects_list, per_page)
    try:
        return paginator.page(page_num)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
