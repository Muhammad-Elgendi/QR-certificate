from django.shortcuts import render
from django.utils import timezone
from certifications.models import Certificate
from django.http import HttpResponse, HttpResponseNotFound

def verify(request,cert_no):
    cert = Certificate.objects.filter(cert_no=cert_no)
    if cert.count() == 1:
        context = {'cert':cert[0]}
        return render(request,'certificate.html',context)
    else:
        return HttpResponseNotFound('<h1>Invalid certificate</h1>')
