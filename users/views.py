from django.shortcuts import render
from .serializer import (
    UserLogInSerializer, 
    UserRegistrationSerializer, 
    UserSerializer, 
    OrganizationSerializer
)
from .models import User, Organization
from rest_framework.generics import RetrieveAPIView, ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserProfileRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(user=User)
    

class UserLogInAPIView(GenericAPIView):
    serializer_class = UserLogInSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "refresh": str(refresh),
            "access": str(access),
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "organization": user.organization_id,
            }
        })
    

class UserLogOutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_refresh_token = request.data['refresh']
        token = RefreshToken(user_refresh_token)
        token.blacklist()
        
        return (token, f"200 OK, “Logout successful”")


class UserRegistrationCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
        

class AllOrganizationUsersListApiView(ListAPIView):
    permission_classes = [IsAuthenticated] # Only supervisor can see all the users
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    