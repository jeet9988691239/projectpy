# filesharing/views.py
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, UploadedFile
from .serializers import CustomUserSerializer, UploadedFileSerializer

class FileUploadView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        if user.user_type != 'OP':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        file = request.FILES.get('file')
        if not file or file.name.split('.')[-1] not in ['pptx', 'docx', 'xlsx']:
            return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = UploadedFile(file=file, uploaded_by=user)
        uploaded_file.save()
        serializer = UploadedFileSerializer(uploaded_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SignUpView(APIView):
    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate and send verification email
            verification_link = f"{settings.SITE_URL}/verify-email/{user.id}/"
            send_mail('Verify your email', f'Please verify your email by clicking on this link: {verification_link}', settings.EMAILCOMPANY, [user.email])
            return Response({'message': 'Sign up successful, please verify your email'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request, user_id, format=None):
        user = CustomUser.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)

class FileDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, file_id, format=None):
        file = UploadedFile.objects.get(id=file_id)
        if not file or request.user.user_type != 'CL':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        download_url = file.get_download_url()
        return Response({'download-link': download_url, 'message': 'success'}, status=status.HTTP_200_OK)
