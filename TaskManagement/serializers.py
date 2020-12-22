from .models import Task, TaskDetail, TaskUpdate
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'created_by', 'task_name',
                  'is_completed', 'created_at', 'last_reviewed']


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDetail
        fields = ['task', 'assigned_to', 'description', 'priority']


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskUpdate
        fields = ['id', 'taskdetail', 'update_info', 'status', 'updated_at']
