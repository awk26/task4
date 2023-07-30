from django.shortcuts import render,HttpResponse,redirect
from .models import FileUpload
from django.contrib.auth.forms import UserCreationForm
from django.contrib  import messages
from .forms import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import pandas as pd
from django.http import Http404





def register(request):
    if request.method=="POST":
        obj=UserCreationForm(request.POST)
        obj.save()
        return redirect("/")
    else:
        d={"form":UserCreationForm}
        return render(request,'register.html ',d)

def loginn(request):
    if request.method=='POST':
        uname=request.POST.get("uname")
        pswd=request.POST.get("pswd")
        user=authenticate(request,username=uname,password=pswd)
        if user is not None:
            request.session["id"]=user.id

            login(request,user)
            return redirect("/Tas-upload")
        else:
            d={'form':LoginForm}
            return render(request,'index.html',d)

    else:
        d={'form':LoginForm}
        return render(request,'index.html',d)


 
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            for file in files:
                 if is_csv_or_excel(file):
                    uploaded_file = FileUpload(file=file,uploaded_by=request.user)
                    uploaded_file.save()
        messages.success(request, 'File uploaded successfully!')               
        return redirect ( '/Tas-upload')
    else:
        form = FileUploadForm()

        return render(request, 'task1.html',{"form":form} )
   

def get_column_names(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.tsv'):
        df = pd.read_csv(file_path, sep='\t')
    elif file_path.endswith('.dsv'):
        encoding_list = ['ascii', 'big5', 'big5hkscs', 'cp037', 'cp273', 'cp424', 'cp437', 'cp500', 'cp720', 'cp737'
                 , 'cp775', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp858', 'cp860', 'cp861', 'cp862'
                 , 'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950'
                 , 'cp1006', 'cp1026', 'cp1125', 'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254'
                 , 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr'
                 , 'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2'
                 , 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'latin_1', 'iso8859_2'
                 , 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9'
                 , 'iso8859_10', 'iso8859_11', 'iso8859_13', 'iso8859_14', 'iso8859_15', 'iso8859_16', 'johab'
                 , 'koi8_r', 'koi8_t', 'koi8_u', 'kz1048', 'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2'
                 , 'mac_roman', 'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_32'
                 , 'utf_32_be', 'utf_32_le', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8', 'utf_8_sig']

        for encoding in encoding_list:
            worked = True
            try:
                df = pd.read_csv(file_path, encoding=encoding, nrows=5)
            except:
                worked = False  
    else:
        raise ValueError('Invalid file format. Only CSV and Excel files are supported.')
    
    return df.columns.tolist()


def data_file(request):
    ids=request.user.id
    user_files = FileUpload.objects.filter(uploaded_by_id=ids)
    source_data=UploadedFile.objects.filter()
    column_names = []
    column_names1=[]
    
    if 'selected_column_name1_list' not in request.session:
        request.session['selected_column_name1_list'] = []
    if 'selected_column_name_list' not in request.session:
        request.session['selected_column_name_list'] = []
    if 'file_name_list' not in request.session:
        request.session['file_name_list'] = []

    # Get previously selected column names from session variables
    selected_column_name1_list = request.session['selected_column_name1_list']
    selected_column_name_list = request.session['selected_column_name_list']
    file_name_list = request.session['file_name_list']

    # Create dataframe with previously selected column names
    if selected_column_name1_list and selected_column_name_list and file_name_list and len(selected_column_name1_list)==len(selected_column_name_list)==len(file_name_list):
        prev_df = pd.DataFrame({
            'Reference Column Name': selected_column_name1_list,
            'Source Column Name': selected_column_name_list,
            'file name': file_name_list
        })
        

    else:
        prev_df = pd.DataFrame(columns=['Reference Column Name', 'Source Column Name','file name'])

    selected_column_name=""
    selected_column_name1=""
    
    new_df=""
    selected_file_dict="" 
    selected_file=""
    if request.method == 'POST':
        selected_file_id = request.POST.get('selected_source_file_id')
        selected_reference_file_id=request.POST.get("selected_reference_file_id")
        if selected_file_id and UploadedFile.objects.filter(id=selected_file_id).exists():
            selected_file = UploadedFile.objects.get(id=selected_file_id)
            selected_file_dict=selected_file.file.name
            column_names1 = get_column_names(selected_file.file.path)
        
        # ... code to get selected file and column names ...
        if selected_reference_file_id and FileUpload.objects.filter(id=selected_reference_file_id).exists():
            reference_file=FileUpload.objects.get(id=selected_reference_file_id)
            column_names=get_column_names(reference_file.file.path)
        selected_column_name=request.POST.get("selected_column_name")
        selected_column_name1=request.POST.get('selected_column_name1')

        # Append current selection to session variables
        selected_column_name_list.append(selected_column_name)
        selected_column_name1_list.append(selected_column_name1)
        file_name_list.append(selected_file_dict)

        request.session['selected_column_name1_list'] = selected_column_name1_list
        request.session['selected_column_name_list'] = selected_column_name_list
        request.session['file_name_list'] = file_name_list
    
        new_df = pd.concat([ prev_df, pd.DataFrame({'Reference Column Name' : [selected_column_name1],
           'Source Column Name'  : [selected_column_name],
             'file name': [selected_file_dict]
         })], ignore_index=True )
       

        new_df['Reference Column Name'].fillna(method='bfill',inplace=True)        
        new_df['Source Column Name'].fillna(method='bfill',inplace=True)
        df = new_df.iloc[::2].reset_index(drop=True)
    
        df.to_csv('new_file.csv',index=False)

    d={"data":user_files,"column_names": column_names,"column_names1":column_names1, "source":source_data,
    "selected_column":selected_column_name1,
    "selected_column1":selected_column_name,"selected_file":selected_file
    }
    return render(request,"sample.html",d)
  

def is_csv_or_excel(file):
    # check if the file has a .csv, .tsv, .dsv, or .xlsx extension
    return file.name.endswith(('.csv', '.tsv', '.dsv', '.xlsx','.xls'))

def upload_files(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            for file in files:
                 if is_csv_or_excel(file):
                    uploaded_file = UploadedFile(file=file)
                    uploaded_file.save()
        messages.success(request, 'File uploaded successfully!')                
        return redirect ( '/Tas-upload')
    else:
        form = FileUploadForm()

        return render(request, 'task1.html',{"form":form} )
    
@login_required
def custom_logout(request):
    ids=request.user
    user_files = FileUpload.objects.filter(uploaded_by_id=ids)
    upload=UploadedFile.objects.filter()
    # Delete each file from the file system
    for file in user_files:
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, file.file.name)):
            os.remove(os.path.join(settings.MEDIA_ROOT, file.file.name))
    # Delete the files from the database
    user_files.delete()
    for file1 in upload:
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, file1.file.name)):
            os.remove(os.path.join(settings.MEDIA_ROOT, file1.file.name))
    upload.delete()        
    # Log the user out
    logout(request)
    # Redirect to the homepage
    return redirect("/")



def download_file(request):
    file_path = 'C:/Users/hp/Desktop/task4/firstproject/new_file.csv'  
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404("page not found")



















        








   


