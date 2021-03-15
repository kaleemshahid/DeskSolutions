from rest_framework.exceptions import NotAcceptable
from .models import User, Profile, Organization, Attendance, ComplaintBox
from .serializers import UserSerializer, OrganizationSerializer, AttendanceSerializer, CreateComplaintBoxSerializer, ListComplaintBoxSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.response import Response
from django.http.request import QueryDict
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


# class AttendanceViewSet(ListAPIView, CreateAPIView, UpdateAPIView):
#     queryset = Attendance.objects.all()
#     serializer_class = AttendanceSerializer
    
#     def create(self, request, *args, **kwargs):
#         """
#         Create attendence of employee/manager
#         """
#         qs = Attendance.objects.filter(user_profile=request.user.id, date=datetime.date.today())
#         if qs:
#             raise NotAcceptable("Already marked for today")
#         request_data = request.data
        
#         if datetime.datetime.now().hour > 9 :
#             request_data.update({
#                 "user_profile": request.user.id,
#                 "is_present" : False
#             })
#         # elif datetime.datetime.now().hour < 8:
#         #     raise NotAcceptable("You can mark attendance after 8.00 am")     
#         else:
#             request_data.update({
#                 "user_profile": request.user.id,
#                 "is_present" : True
#             })
        
#         serializer = self.get_serializer(data=request.data)
#         # print(serializer)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         # headers = self.get_success_headers(serializer.data)
#         # print(serializer.data)
#         # print(datetime.date.today())
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def get_queryset(self):
#         if self.request.user.is_admin:
#             print("asdknasdkn]")
#         return Attendance.objects.filter(user_profile=self.request.user.id)

#     def get_object(self):
#         org = Attendance.objects.get(user_profile=self.request.user.id)
#         print(org)
#         self.check_object_permissions(self.request, org)
#         return org

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    def create(self, request, *args, **kwargs):

        request_data = request.data

        qs = Attendance.objects.filter(user_profile=request.user.id, date=datetime.date.today(), punch_in_time__isnull=False, punch_out_time__isnull=False)
        if qs:
            raise NotAcceptable("Already marked for today")
            
        checkPunchIn =  Attendance.objects.filter(user_profile=request.user.id, date=datetime.date.today(), punch_in_time__isnull=False)
        if checkPunchIn:
            request_data.update({
                "punch_out_time" : datetime.datetime.now()
            })

        print(datetime.datetime.now())

        if datetime.datetime.now().hour > 9 :
            request_data.update({
                "user_profile": request.user.id,
                "is_present" : False
            })
        # elif datetime.datetime.now().hour < 8:
        #     raise NotAcceptable("You can mark attendance after 8.00 am")     
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
        if self.request.user.is_admin:
            print("asdknasdkn]")
        return Attendance.objects.filter(user_profile=self.request.user.id)

    # def partial_update(self, request, pk=None):
    #     obj = self.get_object()
    #     data = request.data
    #     data.update({"user_profile": obj.id})
    #     serializer = AttendanceSerializer(data=data)

    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     print(obj)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def get_object(self):
    #     org = Attendance.objects.get(user_profile=self.request.user.id)
    #     print(org)
    #     self.check_object_permissions(self.request, org)
    #     return org

class ComplaintBoxViewSet(ListAPIView, CreateAPIView):
    queryset = ComplaintBox.objects.all()
    serializer_class = CreateComplaintBoxSerializer

    def create(self, request, *args, **kwargs):
        if self.request.user.is_admin:
            raise NotAcceptable("Admin can not create issue")
        request_data = request.data
        # print(request_data)
        request_data.update({
            "user_profile": request.user.id
        })
        # request.data._mutable = True
        q_dict = QueryDict(mutable=True)
        q_dict.update(request.data)
        # print(q_dict)
        # print(request_data)
        _mutable = q_dict._mutable
        print(_mutable)

        q_dict._mutable = True

        q_dict['subject'] = request_data['subject']
        q_dict['complain'] = request_data['complain']
        print(q_dict['subject'])
        print(request_data['subject'])
        # mutable = request.POST._mutable
        # print(mutable)
        # print(request.POST['subject'])
        # request.POST._mutable = True
        # request.POST['subject'] = 'test data'
        # request.POST._mutable = mutable
        # serializer = self.get_serializer(data=request.data)


        serializer = self.get_serializer(data=q_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print(serializer.data)

        headers = self.get_success_headers(serializer.data)
        # print(serializer.data.copy())
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def post(self, request, *args, **kwargs):
    #     if self.request.user.is_admin:
    #         raise NotAcceptable("Admin can not create issue")
    #     request_data = request.data
    #     # print(request_data)
    #     request_data.update({
    #         "user_profile": request.user.id
    #     })

    #     # request_data._mutable = True
    #     q_dict = QueryDict('', mutable=True)
    #     q_dict.update(request.data)
    #     print(q_dict)
    #     # self.request.data._mutable = True
    #     serializer = self.get_serializer(data=q_dict)
    #     # print(request._request.POST.__dict__) #1
    #     request._request.POST = request._request.POST.copy()
    #     post = request.POST.copy() 
    #     # print(request._request.POST)
    #     # request.data._mutable = True
    #     # print(request.data)
    #     # print(request.data['subject'])
    #     if (subject := request.data.get("subject")) and (
    #         complain := request.data.get("complain")
    #     ):
    #         request.data["subject"] = subject
    #         request.data["complain"] = complain
    #     # request.data._mutable = False

    #     # remember old state
    #     # _mutable = data._mutable
    #     # print(_mutable)
    #     # # set to mutable
    #     # data._mutable = True
    #     # # change the values you want
    #     # data['param_name'] = 'new value'
    #     # # set mutable flag back
    #     # data._mutable = _mutable

    #     # print(request._request.POST.__dict__) #2
    #     # print(request._request.POST) #2
    #     # print(request._request) #2
    #     # print(request) #2
    #     # mydata=request.data.copy()
    #     # print(mydata)
    #     serializer.is_valid(raise_exception=True)
    #     # serializer.create(validated_data=request.data)
    #     serializer.save()
    #     # print(serializer.data)
    #     headers = self.get_success_headers(serializer.data)
    #     # print(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def list(self, request, *args, **kwargs):
        if not self.request.user.is_admin:
            raise NotAcceptable("Employee or manager dont have access to issues")

        queryset = self.filter_queryset(self.get_queryset())
        admin_queryset = ComplaintBox.objects.filter(user_profile__department__organization=request.user.organization)
        serializer = ListComplaintBoxSerializer(admin_queryset, many=True)
        return Response(serializer.data)
