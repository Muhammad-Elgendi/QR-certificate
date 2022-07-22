from django.contrib import admin, messages
from .models import Certificate
from .views import generate_cert_pdf
from django import forms
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.utils.timezone import get_current_timezone
from django.http import FileResponse, HttpResponse
import pandas as pd
import zipfile
import io



class UploadForm(forms.Form):
    file_to_upload = forms.FileField()
    issuer_url = forms.CharField(max_length=2000)

class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'cert_no', 'course_en', 'course_end','get_download_link','get_verify_link']
    list_display_links = ['name_en']

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('upload-certification/',self.upload_certs),
            path('<int:cert_id>/export/',self.download_pdf, name='export_cert'),
            path('exportall/',self.export_certs),

            ]
        return new_urls + urls

    def get_download_link(self, obj):
        return mark_safe('<a href="%s">Download Certificate</a>' % reverse('admin:export_cert', kwargs={'cert_id':obj.id }))
    
    get_download_link.allow_tags = True
    get_download_link.admin_order_field  = 'certificate'  #Allows column order sorting
    get_download_link.short_description = 'Download'  #Renames column head

    def get_verify_link(self, obj):
        return mark_safe('<a href="%s">Verify Certificate</a>' % reverse('certifications:verify', kwargs={'cert_no':obj.cert_no }))
    
    get_verify_link.allow_tags = True
    get_verify_link.admin_order_field  = 'certificate'  #Allows column order sorting
    get_verify_link.short_description = 'Verify'  #Renames column head

    def zipFiles(self,files):
        outfile = io.BytesIO()  # io.BytesIO() for python 3 # StringIO() for python2
        with zipfile.ZipFile(outfile, 'w') as zf:
            for k, v in files.items():
                zf.writestr("{}.pdf".format(k), v.getvalue())
        return outfile.getvalue()



    def export_certs(self,request):
        certs = Certificate.objects.all()     
        if not certs:
            return redirect('admin:index')

        myfiles = {}
        for cert in certs:
            myfile = generate_cert_pdf(request,cert.cert_no,as_IObytes=True)
            myfiles[cert.cert_no] = myfile

        zipped_file = self.zipFiles(myfiles)
        response = HttpResponse(zipped_file, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=Certifications.zip'       
        return response

    def download_pdf(self,request,cert_id):
        try:
            cert = Certificate.objects.get(id=cert_id)
        except Certificate.DoesNotExist:
            raise Http404("Certificate does not exist")
        return generate_cert_pdf(request,cert.cert_no)

    def upload_certs(self,request):
        df = None
        if request.method == "POST":
            certs_file = request.FILES["file_to_upload"]
            cols = {
                'الاسم باللغة العربية':'name_ar',
                'الاسم بالانجليزي  \" للشهادة \"':'name_en',
                'الرقم القومي من اليسار':'national_id',
                'التخصص':'specialization',
                'رقم التليفون':'phone_no',
                'رقم الايصال':'receipt_no',
                'تاريخ الايصال':'receipt_date',
                'رقم الشهادة':'cert_no',
                'اسم الشهادة باللغة العربية':'course_ar',
                'اسم الشهادة باللغة الاجنبية':'course_en',
                'اسم المركز باللغة العربية':'issuer_ar',
                'اسم المركز باللغة الانجليزية':'issuer_en',
                'من':'course_start',
                'إلى':'course_end',
            }

            try:            

                df = pd.read_excel(certs_file,converters= {'من': pd.to_datetime, 'إلى': pd.to_datetime})           
                df['من'].apply(lambda x: x.replace(tzinfo=None))
                df['إلى'].apply(lambda x: x.replace(tzinfo=None))

                # create certifications from the uploaded file
                
                for index, row in df.iterrows():
                    new_cert = {}
                    for col in cols.keys():
                        if pd.notnull(row[col]):
                            new_cert[cols[col]] = row[col]

                    # add issuer url
                    new_cert['issuer_url'] = request.POST["issuer_url"]

                    # create new certification object
                    Certificate.objects.update_or_create(**new_cert)
                        
            except Exception as e:
                print('e:',e)
                messages.warning(request, 'Your File Is Invaild.')                

        form = UploadForm()
        data = {"form":form,
                "df":"Upload Your File To Preview It Here"
                }

        if isinstance(df, pd.DataFrame):
            data.update( { "df": df.to_html() })
            messages.success(request, 'Your File Has Been Uploaded Successfully.')


            
        if request.user.is_active and request.user.is_superuser:
            return render(request,"admin/certifications/certificate/upload.html",data)
        else:
            return redirect('admin:index')

# Register your models here.
# admin.site.register(Certificate)
admin.site.register(Certificate, CertificateAdmin)
