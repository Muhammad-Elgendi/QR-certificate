from django.shortcuts import render

def verify(request):
    context = {}
    return render(request,'certificate.html',context)
