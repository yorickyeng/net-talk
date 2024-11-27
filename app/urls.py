from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>/', views.question, name='one_question'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('ask/', views.ask, name='ask'),
]
