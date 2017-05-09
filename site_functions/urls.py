from django.conf.urls import include, url
from . import views

urlpatterns = [
 	url(r'^$', views.home),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_admin/$', views.admin_register, name='admin_register'),
    url(r'^user_details/(?P<user_id>[0-9]+)$', views.user_detail, name='user_detail'),
    url(r'^upload_receipt/$', views.upload_receipt, name='upload_receipt'),
    url(r'^upload_article/$', views.upload_article, name='upload_article'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^short_course_register/$', views.register_short_course, name='register_short_course'),
    url(r'^short_course_details/(?P<short_course_id>[0-9]+)$', views.short_course_detail, name='short_course_detail'),
    url(r'^talk_details/(?P<talk_id>[0-9]+)$', views.talk_detail, name='talk_detail'),
    url(r'^edit_short_course/(?P<short_course_id>[0-9]+)$', views.edit_short_course, name='edit_short_course'),
    url(r'^edit_talk/(?P<talk_id>[0-9]+)$', views.edit_talk, name='edit_talk'),
    url(r'^mark_payment/(?P<user_id>[0-9]+)$', views.mark_payment, name='mark_payment'),
    url(r'^list_users/$', views.list_students, name='list_users'),
    url(r'^sc_editions/$', views.list_short_courses, name='list_short_courses'),
    url(r'^talk_editions/$', views.list_talks, name='list_talks'),
    url(r'^administration/$', views.administration, name='administration'),
    url(r'^administration/$', views.administration, name='administration'),
    url(r'^accept_article/(?P<user_id>[0-9]+)/(?P<article_id>[0-9]+)$', views.accept_article, name='accept_article'),
    url(r'^download/(?P<path>.*)$', views.download, name='download'),
    url(r'^confirm/(?P<confirmation_code>.*)/(?P<user_id>[0-9]+)$', views.confirm, name='confirm'),
    url(r'^talk_register/$', views.register_talk, name='register_talk'),
]
