from django.contrib import admin

from .models import *

admin.site.register(FileUpload)
admin.site.register(UploadedFile)