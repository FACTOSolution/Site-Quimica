from django.conf.urls import include, url
from . import views

urlpatterns = [
 	url(r'^$', views.home),
    url(r'^register/$', views.register, name='register'),
    url(r'^upload_receipt/$', views.upload_receipt, name='upload_receipt'),
]
