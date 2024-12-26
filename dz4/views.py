from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect

from dz4.models import Question, Tag, Answer, Profile, SignupForm

top_tags = Tag.objects.annotate(question_count=Count('question')).order_by('-question_count')[:8]

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
    auth_user = check_auth(request)

    return render(request, 'index.html', {'auth': auth_user, 'tags':top_tags,'questions':page.object_list,'tag': tag, 'page_obj':page,})
def render_hot_questions_page(request):
    return render_questions_list_page(request,'hot')
def render_questions_with_tag_page(request, tag):
    return render_questions_list_page(request,tag=tag)
def render_ask_page(request):
    auth_user = check_auth(request)
    return render(request, 'ask.html', {'auth': auth_user, 'tags': top_tags})
def render_question_page(request,id):
    auth_user = check_auth(request)
    question = Question.objects.annotate(total_marks=Sum('questionlike__mark')).get(id=id)
    answers = Answer.objects.annotate(total_marks=Coalesce(Sum('answerlike__mark'), 0)).filter(question=id).order_by('-total_marks')
    page = paginate(answers, request, 30)
    return render(request, 'question.html',{'auth': auth_user, 'tags': top_tags, 'question':question, 'page_obj':page,})
def render_settings_page(request):
    auth_user = check_auth(request)
    return render(request, 'settings.html', {'auth': auth_user, 'tags': top_tags})
def render_login_page(request):
    error_message = None
    continue_url = request.GET.get('continue', '/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(continue_url)  # Перенаправление после успешного входа
        else:
            error_message = "Неверный пароль или аккаунта не существует."

    return render(request, 'login.html', {'error_message': error_message})
def render_signup_page(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохраняем пользователя
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Хешируем пароль
            user.save()

            # Создаем профиль
            profile = Profile.objects.create(
                user=user,
                nickname=form.cleaned_data.get('nickname'),
                user_img=form.cleaned_data.get('user_img')
            )

            # Логиним пользователя после регистрации
            login(request, user)

            return render_questions_list_page(request)  # Перенаправляем на главную страницу
        else:
            # Если форма невалидна, просто возвращаем шаблон с ошибками
            return render(request, 'signup.html', {'form': form,'tags': top_tags})
    else:
        form = SignupForm()  # Инициализируем форму для GET запроса

    # Возвращаем страницу с пустой или предварительно заполненной формой
    return render(request, 'signup.html', {'form': form, 'tags': top_tags})
def logout_user(request):
    logout(request)
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
def questions_sort(sort):
    if sort == None:
        return Question.objects.order_by_mark()
    else:
        return Question.objects.order_by_date()
def check_auth(request):
    auth_user = request.user
    if auth_user.is_authenticated:
        user = Profile.objects.get(user_id=auth_user.id)
        return user
    else:
        return None