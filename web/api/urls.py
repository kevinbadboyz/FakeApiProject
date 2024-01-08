from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    LoginView, 
    TodoListApiView, TodoDetailApiView,    
    PostListApiView, PostDetailApiView,
)
app_name = 'api'

urlpatterns = [    
    path('api/v1/login', LoginView.as_view()),    
    path('api/todo', TodoListApiView.as_view()),
    path('api/todo/<int:id>', TodoDetailApiView.as_view()),    
    path('api/post', PostListApiView.as_view()),
    path('api/post/<int:id>', PostDetailApiView.as_view()),    
]

