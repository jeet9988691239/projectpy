# filesharing/urls.py
from django.urls import path
from .views import FileUploadView, SignUpView, VerifyEmailView, FileDownloadView

urlpatterns = [
    path('upload-file/', FileUploadView.as_view(), name='file_upload'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('verify-email/<int:user_id>/', VerifyEmailView.as_view(), name='verify_email'),
    path('download-file/<int:file_id>/', FileDownloadView.as_view(), name='file_download'),
]
