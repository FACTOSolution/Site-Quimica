from django.conf.urls import include, url
from . import views

urlpatterns = [
 	url(r'^$', views.home),
    url(r'^register/$', views.register, name='register'),
]