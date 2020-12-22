from django.urls import path
from .views import GetTask, CreateTask

urlpatterns = [
    path('<int:pk>/', GetTask.as_view()),
    path('createtask/', CreateTask.as_view()),
]
