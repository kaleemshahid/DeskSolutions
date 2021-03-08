from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TaskManagementViewSet, SubTaskViewSet

router = DefaultRouter()
router.register(r'subtask', SubTaskViewSet)
router.register(r'', TaskManagementViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
