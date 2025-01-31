"""
URL configuration for web_dz1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dz1 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.render_questions_list_page, name='list_page_url'),
    path('new_question/', views.render_ask_page, name='ask_page_url'),
    path('question/', views.render_question_page, name='question_page_url'),
    path('login/',views.render_login_page,name='login_page_url'),
    path('logout/',views.logout,name='logout_url'),
    path('signup/',views.render_signup_page,name='signup_page_url'),
]
