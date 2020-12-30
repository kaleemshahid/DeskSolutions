from .models import Task, TaskDetail, TaskUpdate
from .serializers import TaskSerializer, TaskDetailSerializer, TaskUpdateSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from account.models import Department


class AdminTaskManagementViewSet(ListAPIView, RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskManagementViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        Returns the queryset of task for a a login manager
        """
        return Task.objects.filter(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.user.is_admin:
            # tasks queryset against an admin
            queryset = Task.objects.filter(created_by__profile__department__organization=request.user.organization)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubTaskViewSet(ModelViewSet):
    queryset = TaskDetail.objects.all()
    serializer_class = TaskDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        update_history_queryset = TaskUpdate.objects.filter(taskdetail=instance.id)
        update_history_data = TaskUpdateSerializer(update_history_queryset, many=True).data
        response = serializer.data
        response.update({"update_history": update_history_data})
        return Response(response)

    def list(self, request, *args, **kwargs):
        # for manager
        if request.data.get("parent_task_id"):
            queryset = self.filter_queryset(self.get_queryset()).filter(task=request.data.get("parent_task_id"))
        # for employee
        elif not request.data.get("parent_task_id"):
            queryset = self.filter_queryset(self.get_queryset()).filter(assigned_to=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        make a new entry(history) in TaskUpdate model on every update request
        """

        instance = self.get_object()
        data = request.data
        data.update({"taskdetail": instance.id})

        serializer = TaskUpdateSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
