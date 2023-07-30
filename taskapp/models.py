from django.db import models
import os
from django.contrib.auth.models import User

class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name
    
def get_upload_path(instance, filename):
    # construct the upload path dynamically based on the filename
    return os.path.join('uploads', filename)    


class UploadedFile(models.Model):
    file = models.FileField(upload_to=get_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.file.name







