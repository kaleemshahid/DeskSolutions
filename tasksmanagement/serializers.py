from .models import Task, TaskDetail,  TaskUpdate
from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable


class TaskSerializer(serializers.ModelSerializer):
    manager_name = serializers.SerializerMethodField()

    def get_manager_name(self, obj):
        names = {
            "first_name": obj.created_by.first_name,
            "last_name": obj.created_by.last_name
        }
        return names

    class Meta:
        model = Task
        fields = ['id', 'task_name',
                  'is_completed', 'created_at', 'last_reviewed', 'manager_name']

    def create(self, validated_data):
        name = validated_data.get('task_name')
        user = self.context['request'].user

        if user.is_admin:
            raise NotAcceptable("Admin can not create a task")

        task = Task.objects.create(task_name=name, created_by=user)

        task.save()
        return task


class TaskDetailSerializer(serializers.ModelSerializer):
    assignee_name = serializers.SerializerMethodField()
    update_history = serializers.SerializerMethodField()

    def get_assignee_name(self, obj):
        names = {
            "first_name": obj.assigned_to.first_name,
            "last_name": obj.assigned_to.last_name
        }
        return names

    def get_update_history(self, obj):
        update_history_queryset = TaskUpdate.objects.filter(taskdetail=obj.id)
        update_history_data = TaskUpdateSerializer(update_history_queryset, many=True).data

        return update_history_data

    class Meta:
        model = TaskDetail
        fields = ['id', 'task', 'assigned_to', 'assignee_name', 'description', 'start_time', 'end_time', 'priority', 'update_history']


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskUpdate
        fields = ['taskdetail', 'update_info', 'status', 'updated_at']
