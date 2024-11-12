from django.shortcuts import render

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
def render_questions_list_page(request):
    return render(request, 'index.html', {'auth': True, 'tags':tags, 'tag': None, 'sort': None})
def render_hot_questions_page(request):
    return render(request, 'index.html', {'auth': True, 'tags':tags, 'tag': None, 'sort': 'Hot'})
def render_questions_with_tag_page(request, tag):
    return render(request, 'index.html', {'auth': True, 'tags': tags, 'tag': tag})
def render_ask_page(request):
    return render(request, 'ask.html')
def render_question_page(request):
    return render(request, 'question.html')
def render_login_page(request):
    return render(request, 'login.html')
def render_signup_page(request):
    return render(request, 'signup.html')
def logout(request):
    return render(request, 'index.html', {'auth': False, 'tags':tags, 'tag': None})