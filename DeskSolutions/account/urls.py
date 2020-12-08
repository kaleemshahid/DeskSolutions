# django imports
from django.urls import include, path
# rest-framework imports
from rest_framework.routers import DefaultRouter
from .views import UserLoginApiView

urlpatterns = [
    path('login/', UserLoginApiView.as_view(), name="login")
]
