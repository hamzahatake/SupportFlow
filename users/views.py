from django.shortcuts import render
from .serializer import UserLogInSerializer, UserRegistrationSerializer, UserSerailizer, OrganizationSerializer
from .models import User, Organization
from rest_framework.generics import RetrieveAPIView, ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserProfileRetrieveView(RetrieveAPIView):
    permission_class = [IsAuthenticated]
    serializer_class = UserSerailizer

    def get_queryset(self):
        return UserSerailizer.objects.filter(user=User)
    

class UserLogInAPIView(GenericAPIView):
    serializer_class = UserLogInSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            raise ValidationError("Invalid credentials!")

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
    

class UserRegistrationCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
        

class AllOrganizationUsersListApiView(ListAPIView):
    permission_classes = [IsAuthenticated] # Only supervisor can see all the users
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        organization_users = self.request.user.organization
        return organization_users
    