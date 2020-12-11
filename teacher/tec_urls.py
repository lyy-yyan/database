from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'tec_login/', views.tec_login, name= 'tec_login'),
    url(r'tec_regist/', views.tec_regist, name= 'tec_regist'),
    url(r'tec_manage/', views.tec_manage, name= 'tec_manage'),
    url(r'tec_check/', views.tec_check, name= 'tec_check'),
    url(r'tec_sign/', views.tec_sign, name= 'tec_sign'),
    url(r'tec_massage/(?P<nid>\d+)', views.tec_massage, name= 'tec_massage'),
    url(r'^del_stu/(?P<nid>\d+)', views.del_stu, name='del_stu'),
    # url(r'^image/(?P<news_id>.+)/$',views.my_image,name="image")
    # url(r'makeQrcode/', views.makeQrcode, name= 'makeQrcode'),
]