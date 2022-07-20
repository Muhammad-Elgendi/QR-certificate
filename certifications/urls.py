from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('<slug:cert_no>', views.verify, name='verify'),
]


