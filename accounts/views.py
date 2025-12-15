from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from .models import User
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, ProfileSerializer
from .tokens import email_verification_token
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        token = email_verification_token.make_token(user)
        uid = user.pk
        current_site = get_current_site(self.request)
        verify_url = f"http://{current_site.domain}{reverse('accounts:verify-email')}?token={token}&uid={uid}"
        message = f"Hi {user.email},\n\nPlease verify your email by visiting:\n{verify_url}\n\nThanks!"
        send_mail("Verify your email", message, None, [user.email])

class VerifyEmailView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = request.GET.get("token")
        uid = request.GET.get("uid")
        user = get_object_or_404(User, pk=uid)
        if email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"detail": "Email verified"}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile