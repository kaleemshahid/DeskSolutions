from django.shortcuts import render
from .models import Task, TaskDetail, TaskUpdate
from .serializers import TaskSerializer, TaskDetailSerializer, TaskUpdateSerializer
from rest_framework import generics
from rest_framework.decorators import permission_classes


class GetTask(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class CreateTask(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
