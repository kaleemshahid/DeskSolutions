from django.shortcuts import render
from .models import User, Profile
from .serializers import UserSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


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
        profiles = Profile.objects.filter(organization=token.user_id)
        role = "admin"
        if not profiles:
            pass
        elif profiles.first().is_manager:
            role = "manager"
        elif not profiles.first().is_manager:
            role = "employee"

        return Response(
            {
                'token': token.key,
                'role': role,
                'first_name':token.user.first_name,
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


# m1 vvqsXO6
# e1 b0Lapi8   iX6fZcm
# e2 aNLyzev