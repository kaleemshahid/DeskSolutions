from .models import Task, TaskDetail,  TaskUpdate
from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'task_name',
                  'is_completed', 'created_at', 'last_reviewed']

    def create(self, validated_data):
        name = validated_data.get('task_name')
        user = self.context['request'].user

        if user.is_admin:
            raise NotAcceptable("Admin can not create a task")

        task = Task.objects.create(task_name=name, created_by=user)

        task.save()
        return task


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDetail
        fields = '__all__'


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskUpdate
        fields = ['id', 'taskdetail', 'update_info', 'status', 'updated_at']
