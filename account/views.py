from .models import User, Profile, Organization, Attendance
from .serializers import UserSerializer, OrganizationSerializer, AttendanceSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginApiView(ObtainAuthToken):
    """ Handle creating user authentication tokens """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # delete old token and assign a new one for evey login request
        if not created:
            token.delete()
            token = Token.objects.create(user=user)

        # getting role of the login user
        profiles = Profile.objects.filter(user=token.user_id)
        role = "admin"
        if not profiles:
            pass
        elif profiles.first().is_manager:
            role = "manager"
        elif not profiles.first().is_manager:
            role = "employee"

        print(role)

        return Response(
            {
                'token': token.key,
                'role': role,
                'first_name': token.user.first_name,
                'last_name': token.user.last_name,
                'created_at': token.user.date_joined,

            }
        )


class LogoutApiView(APIView):
    """Handles logout"""

    def post(self, request):
        print(request.user.email)
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeViewSet(ListAPIView):

    def list(self, request, *args, **kwargs):
        manager_queryset = Profile.objects.filter(user=request.user)
        employees_queryset = Profile.objects.filter(department=manager_queryset.first().department, is_manager=False)

        employees = []
        for emp in employees_queryset:
            employees.append({'id': emp.user.id, "first_name": emp.user.first_name,
                              "last_name": emp.user.last_name})
        return Response(employees)


class OrganizationViewSet(UpdateAPIView):
    serializer_class = OrganizationSerializer

    def update(self, request, *args, **kwargs):
        orgs = Organization.objects.get(user=request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


class AttendanceViewSet(ListAPIView, CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def create(self, request, *args, **kwargs):
        """
        Create attendence of employee/manager
        """
        request_data = request.data
        request_data.update({
            "user_profile": request.user.id
        })
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        return Attendance.objects.filter(user_profile=self.request.user.id)
