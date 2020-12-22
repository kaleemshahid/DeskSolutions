from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ManagerTaskManagementViewSet, SubTaskViewSet

router = DefaultRouter()
router.register(r'manager', ManagerTaskManagementViewSet)
router.register(r'subtask', SubTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
