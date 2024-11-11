from django.shortcuts import render


def render_questions_list_page(request):
    return render(request, 'index.html')
def render_ask_page(request):
    return render(request, 'ask.html')
def render_question_page(request):
    return render(request, 'question.html')