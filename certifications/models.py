from django.db import models


class Issuer(models.Model):
    name_ar = models.CharField('Issuer Name In Arabic', max_length=100)
    name_en = models.CharField('Issuer Name In English', max_length=100)
    url = models.CharField('Verify URL', max_length=2000)
    signature = models.ImageField(upload_to='signatures', blank=True)

    def __str__(self):
        return self.name_en

    


'''
م
الاسم باللغة العربية
الاسم بالانجليزي  " للشهادة "
الرقم القومي من اليسار
التخصص
رقم التليفون
رقم الايصال
تاريخ الايصال
رقم الشهادة
اسم الشهادة باللغة العربية
اسم الشهادة باللغة الاجنبية
اسم المركز باللغة العربية
اسم المركز باللغة الانجليزية
من
إلى

'''
class Certificate(models.Model):

    name_ar = models.CharField('Name In Arabic', max_length=100)
    name_en = models.CharField('Name In English', max_length=100)
    national_id = models.IntegerField('National Identification Number', blank=True, null=True)
    image = models.ImageField(upload_to='images', blank=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    phone_no = models.IntegerField('Phone Number', blank=True, null=True)
    receipt_no = models.IntegerField('Receipt Number', blank=True, null=True)
    receipt_date = models.DateTimeField('Receipt Issued Time', blank=True, null=True)
    cert_no = models.CharField('Certification Number', max_length=40, unique=True)
    course_ar = models.CharField('Course In Arabic', max_length=100)
    course_en = models.CharField('Course In English', max_length=100)
    course_type_en =  models.CharField('Course Type In English', max_length=100)
    course_type_ar =  models.CharField('Course Type In Arabic', max_length=100)
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE)
    course_start = models.DateTimeField('Course Started Time', blank=True, null=True)
    course_end = models.DateTimeField('Course Ended Time')
    issue_date = models.DateTimeField('Certification Issued Time', blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return self.name_en+' | No. '+self.cert_no
