from django.shortcuts import render


def render_main_page(request):
    return render(request,'index.html')