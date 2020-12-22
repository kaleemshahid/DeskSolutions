"""ProjectDeskSolutions3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from account.serializers import UserSerializer
from account.views import UserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include('rest_framework.urls')),
    path('api/', include('account.urls')),
    path('api/task/', include('TaskManagement.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('home/', include('desksolutionsbase.urls', namespace='signup')),
    path('task/', include('TaskManagement.urls')),
]

if settings.DEBUG:
    #     urlpatterns += static(settings.STATIC_URL,
    #                           document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)