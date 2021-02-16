from rest_framework.exceptions import NotAcceptable
from .models import User, Profile, Organization, Attendance, ComplaintBox
from .serializers import UserSerializer, OrganizationSerializer, AttendanceSerializer, CreateComplaintBoxSerializer, ListComplaintBoxSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.response import Response
import datetime


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

        location = {
            'lat': token.user.organization.latitude,
            'long': token.user.organization.longitude,
            'radius': token.user.organization.radius
        }

        return Response(
            {
                'token': token.key,
                'role': role,
                'first_name': token.user.first_name,
                'last_name': token.user.last_name,
                'created_at': token.user.date_joined,
                'organization_location': location

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
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_object(self):
        org = User.objects.get(id=self.request.user.id).organization
        print(org)
        self.check_object_permissions(self.request, org)
        return org


class AttendanceViewSet(ListAPIView, CreateAPIView, UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create attendence of employee/manager
        """
        qs = Attendance.objects.filter(user_profile=request.user.id, punch_in_time=datetime.date.today())
        if qs:
            raise NotAcceptable("Already marked for today")
        request_data = request.data
        
        if datetime.datetime.now().hour > 9 :
            request_data.update({
                "user_profile": request.user.id,
                "is_present" : False
            })
        elif datetime.datetime.now().hour < 8:
            raise NotAcceptable("You can mark attendance after 8.00 am")     
        else:
            request_data.update({
                "user_profile": request.user.id,
                "is_present" : True
            })
        
        serializer = self.get_serializer(data=request.data)
        # print(serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # print(serializer.data)
        # print(datetime.date.today())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Attendance.objects.filter(user_profile=self.request.user.id)

    def get_object(self):

        org = Attendance.objects.get(user_profile=self.request.user.id)
        print(org)
        self.check_object_permissions(self.request, org)
        return org


class ComplaintBoxViewSet(ListAPIView, CreateAPIView):
    queryset = ComplaintBox.objects.all()
    serializer_class = CreateComplaintBoxSerializer

    def create(self, request, *args, **kwargs):
        """
        Create complaint
        """
        if self.request.user.is_admin:
            raise NotAcceptable("Admin can not create issue")
        request_data = request.data
        request_data.update({
            "user_profile": request.user.id
        })
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        if not self.request.user.is_admin:
            raise NotAcceptable("Employee or manager dont have access to issues")

        queryset = self.filter_queryset(self.get_queryset())
        admin_queryset = ComplaintBox.objects.filter(user_profile__department__organization=request.user.organization)
        serializer = ListComplaintBoxSerializer(admin_queryset, many=True)
        return Response(serializer.data)
