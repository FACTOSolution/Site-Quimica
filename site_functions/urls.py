from django.conf.urls import include, url
from . import views

urlpatterns = [
 	url(r'^$', views.home),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_details/$', views.user_detail, name='user_detail'),
    url(r'^upload_receipt/$', views.upload_receipt, name='upload_receipt'),
    url(r'^upload_article/$', views.upload_article, name='upload_article'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^short_course_register/$', views.register_short_course, name='short_course_register'),
    url(r'^short_course/(?P<short_course_id>[0-9]+)$', views.short_course_detail, name='short_course'),
    url(r'^edit_short_course/(?P<short_course_id>[0-9]+)$', views.edit_short_course, name='edit_short_course'),
]
