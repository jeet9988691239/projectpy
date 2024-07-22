from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta

# Custom user model
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('OP', _('Operation User')),
        ('CL', _('Client User')),
    )
    user_type = models.CharField(max_length=2, choices=USER_TYPE_CHOICES)

# File model
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def get_download_url(self):
        # Generate a secure URL for file download
        base_url = reverse('file_download', args=[self.id])
        token = get_random_string(length=32)
        return f"{base_url}?token={token}"
