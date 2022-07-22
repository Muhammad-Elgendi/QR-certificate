from django.urls import path

from . import views

app_name = "certifications"

urlpatterns = [
    # path('', views.index, name='index'),
    path('<slug:cert_no>', views.verify, name='verify'),
    # path('download/<slug:cert_no>', views.generate_cert_pdf, name='generate_cert'),
]


