from django.db import models
from django.utils import timezone
from uuid import uuid4

class UploadedFile(models.Model):
    file_id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    upload_date = models.DateTimeField(default = timezone.now)
    row_count = models.IntegerField()
    file = models.FileField(upload_to='uploads/', null=True, blank=True)

class UserData(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='data')
    sno = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    date_of_birth = models.DateField()

    class Meta:
        unique_together = ('first_name', 'last_name')