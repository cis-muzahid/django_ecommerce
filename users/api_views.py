from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string

from .models import CustomUser, Role, Permission, UserAddress
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    ChangePasswordSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer,
    TokenSerializer, RoleSerializer, PermissionSerializer, UserAddressSerializer
)
from drf_spectacular.utils import extend_schema


@extend_schema(
    request=UserRegistrationSerializer,
    responses=UserSerializer,
    auth=[]
)

class UserRegistrationView(APIView):
    """API view for user registration"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
                # 'tokens': {
                #     'access': str(refresh.access_token),
                #     'refresh': str(refresh)
                # }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=UserLoginSerializer,
    auth=[]
)

class UserLoginView(APIView):
    """API view for user login"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            # Update last login
            login(request, user)
            
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """API view for user logout"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            logout(request)
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """API view for user profile management"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get user profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Update user profile"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """API view for changing password"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    """API view for password reset request"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)
            
            # Generate reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Send reset email (you can customize this)
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            
            # For now, just return the reset URL (in production, send email)
            return Response({
                'message': 'Password reset email sent',
                'reset_url': reset_url  # Remove this in production
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """API view for password reset confirmation"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, uid, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(pk=user_id)
            
            if default_token_generator.check_token(user, token):
                serializer = PasswordResetConfirmSerializer(data=request.data)
                if serializer.is_valid():
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()
                    
                    return Response({
                        'message': 'Password reset successful'
                    }, status=status.HTTP_200_OK)
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'error': 'Invalid or expired token'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({
                'error': 'Invalid reset link'
            }, status=status.HTTP_400_BAD_REQUEST)


# ViewSets for CRUD operations
class UserViewSet(ModelViewSet):
    """ViewSet for User management (Admin only)"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['is_active', 'user_role']
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'last_login']
    
    def get_permissions(self):
        """Only admin users can manage other users"""
        if self.action in ['list', 'create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
            # Add custom permission check for admin role
            if hasattr(self.request.user, 'user_role') and self.request.user.user_role:
                if self.request.user.user_role.name not in ['admin'] and not self.request.user.is_superuser:
                    permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]


class RoleViewSet(ModelViewSet):
    """ViewSet for Role management"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    search_fields = ['name']
    
    def get_permissions(self):
        """Allow anyone to list roles (for signup), but only admin can create/edit/delete"""
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.AllowAny()]
        
        # For create, update, delete - require admin
        if hasattr(self.request.user, 'user_role') and self.request.user.user_role:
            if self.request.user.user_role.name not in ['admin'] and not self.request.user.is_superuser:
                return [permissions.IsAdminUser()]
        return [permissions.IsAdminUser()]


class PermissionViewSet(ModelViewSet):
    """ViewSet for Permission management"""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']
    
    def get_permissions(self):
        """Only admin users can manage permissions"""
        if hasattr(self.request.user, 'user_role') and self.request.user.user_role:
            if self.request.user.user_role.name not in ['admin'] and not self.request.user.is_superuser:
                return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class UserAddressViewSet(ModelViewSet):
    """ViewSet for User Address management"""
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Users can only access their own addresses"""
        return UserAddress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set the user when creating an address"""
        # If this is the first address, make it default
        if not UserAddress.objects.filter(user=self.request.user).exists():
            serializer.save(user=self.request.user, is_default=True)
        else:
            # If setting as default, unset other defaults
            if serializer.validated_data.get('is_default', False):
                UserAddress.objects.filter(user=self.request.user).update(is_default=False)
            serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """Handle default address updates"""
        if serializer.validated_data.get('is_default', False):
            UserAddress.objects.filter(user=self.request.user).update(is_default=False)
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """Set an address as default"""
        address = self.get_object()
        UserAddress.objects.filter(user=request.user).update(is_default=False)
        address.is_default = True
        address.save()
        
        return Response({
            'message': 'Default address updated successfully'
        }, status=status.HTTP_200_OK)