from .models import Task, TaskDetail, TaskUpdate
from .serializers import TaskSerializer, TaskDetailSerializer, TaskUpdateSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
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

    def list(self, request, *args, **kwargs):
        if request.data.get("parent_task_id"):
            queryset = self.filter_queryset(self.get_queryset()).filter(task=request.data.get("parent_task_id"))
        elif not request.data.get("parent_task_id"):
            queryset = self.filter_queryset(self.get_queryset()).filter(assigned_to=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
