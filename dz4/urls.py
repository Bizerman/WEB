"""
URL configuration for web_dz4 project.

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from dz4 import views
from web_dz4 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.render_questions_list_page, name='list_page_url'),
    path('hot', views.render_hot_questions_page, name='list_hot_questions_page'),
    path('tag/<str:tag>', views.render_questions_with_tag_page, name='list_tag_url'),
    path('ask/', views.render_ask_page, name='ask_page_url'),
    path('settings',views.render_settings_page, name='settings_page_url'),
    path('question/<int:id>', views.render_question_page, name='question_page_url'),
    path('login/',views.render_login_page,name='login_page_url'),
    path('logout/',views.logout,name='logout_url'),
    path('signup/',views.render_signup_page,name='signup_page_url'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
