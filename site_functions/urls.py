from django.conf.urls import include, url
from . import views

urlpatterns = [
 	url(r'^$', views.home),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_details/$', views.user_detail, name='user_detail'),
    url(r'^upload_receipt/$', views.upload_receipt, name='upload_receipt'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
]