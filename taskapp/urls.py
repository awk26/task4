from django.urls import path
from .import views as v 

urlpatterns = [
    path("reg",v.register,name="register"),
    path("login",v.loginn,name="login"),
    path('upload',v. upload_file, name='file_upload'),
    path('load_files',v.data_file , name='load_files'),
    path('upload/', v.upload_files, name='upload_files'),
    path('logout/', v.custom_logout, name='logout'),
    path('download/',v.download_file, name='download_file'),
    


]
