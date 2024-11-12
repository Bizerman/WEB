from django.shortcuts import render


def render_questions_list_page(request):
    return render(request, 'index.html', {'auth': True})
def render_ask_page(request):
    return render(request, 'ask.html')
def render_question_page(request):
    return render(request, 'question.html')
def render_login_page(request):
    return render(request, 'login.html')
def render_signup_page(request):
    return render(request, 'signup.html')
def logout(request):
    return render(request, 'index.html', {'auth': False})