from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^upload/$', views.UploadFileView.as_view(), name='upload'),
    url(r'^list/$', views.UploadFileList.as_view(), name='list'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]
