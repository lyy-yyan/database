from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'index/', views.index, name= 'index'),
    url(r'stu_check/', views.stu_check, name= 'stu_check'),
    url(r'stu_sign(?P<nid>\d+)$', views.stu_sign, name= 'stu_sign'),
    url(r'stu_acc/', views.stu_acc, name= 'stu_acc'),
]