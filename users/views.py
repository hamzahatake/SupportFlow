from django.shortcuts import render
from .serializer import UserLogInSerializer, UserRegistrationSerializer, UserSerializer, OrganizationSerializer
from .models import User, Agent, Supervisor
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.views import APIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from rest_framework import status
from .permissions import CanCreateUser

    
# User Authentication Views

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
    

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = User.object.create(user=request.data, role="customer") if invite_token else self.request.user


class UserLogOutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh = request.data.get("refresh")
        
        if not refresh:
            return Response({"error": "Refresh token required"}, status=400)
       
        token = RefreshToken(refresh)
        token.blacklist()
        
        return (token, f"200 OK, “Logout successful”")


class TokenRefreshView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *arg, **kwargs):
        refresh_token = request.data.get("refresh")
        
        if not refresh_token:
            return AuthenticationFailed({"error": "Refresh token required"}, status=400)
        
        try:
            token = RefreshToken(refresh_token)
            new_access = str(token.access_token)

            return Response(
                {"access": new_access},
                status=status.HTTP_200_OK
            )
        except TokenError as e:
            raise AuthenticationFailed("Invalid or expired refresh token.")
        

class PasswordResetView(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "Invalid email format."},
                status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "If this email is registered, you’ll receive a password reset link shortly."},
                status=status.HTTP_200_OK)
        
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"https://yourfrontend.com/reset-password/{uid}/{token}"

        send_mail(
            subject="Password Reset Request",
            message=f"Click the link below to reset your password:\n{reset_link}",
            from_email="no-reply@yourdomain.com",
            recipient_list=[email],
            fail_silently=True,
        )

        return Response(
            {"message": "If this email is registered, you’ll receive a password reset link shortly."},
            status=status.HTTP_200_OK
        )
    

class PasswordResetConfirmView(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *arg, **kwargs):
        uidb64 = request.data.get("uidb64")
        token = request.data.get("token")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if not password or not confirm_password:
            return Response("Password fields are required.")
        if password != confirm_password:
            return Response("Password do not match.")
        validate_password(password)
   
        
        decode_uid = force_str(urlsafe_base64_decode(uidb64))
        try:
            user = User.objects.get(pk=decode_uid)
        except User.DoesNotExist:
            return Response("Invalid link.")

        
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response("Invalid or expired token", status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response("Password reset successful.")


# User Profile Management

class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk:
            user = User.objects.get(pk=pk) 
        else:
            user = self.request.user
       
        if self.request.user.role == "Customer" and user != self.request.user:
            raise PermissionDenied("You cannot access this profile.")
        if user.organization != self.request.user.organization:
            raise PermissionDenied("Organization mismatch")
        
        return user
        
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        return super().update(request, *args, **kwargs)
    

class UserListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role', 'organization']

    def get_queryset(self):
        user = self.request.user
        if user.role == "customer":
            queryset = User.objects.filter(pk=user.pk)
        elif user.role == "agent":
            queryset = User.objects.filter(department=user.department)
        elif user.role == "supervisor":
            queryset = User.objects.filter(organization=user.organization)
        elif user.role == "admin":
            queryset = User.objects.all()
        else:
            raise PermissionDenied("Not allowed.")
        
        queryset = queryset.filter(organization=self.request.user.organzation)


class UserCreateView(CreateAPIView):
    permission_classes = [CanCreateUser]
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)