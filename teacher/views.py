import base64
import os

from MyQR import myqr
import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
import random
import string

from django.utils import timezone #引入timezone模块
from . import models

from django.http import HttpResponse
# Create your views here.
tec_num = '170101'
tec_password = '000'
authority = '1234'
tec_name = 'xxx'
message = ''

def tec_login(request):
    # return render(request,"teacher/templates/tec_login.html")
    global tec_num, tec_password, authority, message
    if request.method == "POST":
        tec_num = request.POST.get("tec_num", None)
        tec_password = request.POST.get("tec_password", None)
        authority = request.POST.get("authority", None)
        teacher = models.Teacher.objects.filter(tec_num=tec_num)
        if teacher.exists() and tec_password == models.Teacher.objects.get(tec_num=tec_num).tec_password:
            if authority == "1234":
                return render(request, 'tec_check.html', {'teacher': models.Teacher.objects.get(tec_num=tec_num)})
            else:
                messages.success(request, "权限码有误，请重新登录")
                return render(request, 'tec_login.html')
        else:
            messages.success(request, "账号或密码有误，请重新登录")
            return render(request, 'tec_login.html')
    else:
        return render(request, "tec_login.html")

def tec_check(request):
    return render(request,"tec_check.html")

def tec_regist(request):
    global message, tec_num, tec_name, tec_course, tec_password, authority
    if request.method == "POST":
        tec_num = request.POST.get("tec_num", None)
        tec_name = request.POST.get("tec_name", None)
        tec_course = request.POST.get("tec_course", None)
        tec_password = request.POST.get("tec_password", None)
        authority = request.POST.get("authority", None)
        if authority == "1234":
            if models.Teacher.objects.filter(tec_num=tec_num).exists():
                messages.success(request, "该工号已存在，添加失败")
                return render(request, "tec_regist.html")
            else:
                models.Teacher.objects.create(tec_num=tec_num, tec_name=tec_name, tec_course=tec_course,
                                              tec_password=tec_password)
                messages.success(request, "注册成功，请返回登录")
                return render(request, "tec_regist.html")
        else:
            messages.success(request, "权限码错误，注册失败")
            return render(request, "tec_regist.html")
    else:
        return render(request, "tec_regist.html")

def tec_manage(request):
    global student, message

    if request.method == 'POST':
        stu_num = request.POST.get("stu_num", None)
        stu_name = request.POST.get("stu_name", None)
        stu_major = request.POST.get("stu_major", None)
        stu_class = request.POST.get("stu_class", None)
        if stu_num == '':
            messages.success(request, "账号不能为空，请重写")
            return redirect('/teacher/tec_manage')
        if stu_name == '':
            messages.success(request, "姓名不能为空，请重写")
            return redirect('/teacher/tec_manage')
        if stu_major == '':
            stu_major = "计算机科学与技术"
        if stu_class == '':
            messages.success(request, "班级不能为空，请重写")
            return redirect('/teacher/tec_manage')
        if models.Student.objects.filter(stu_num=stu_num).exists():
            messages.success(request, "该学号已存在，添加失败")
        else:
            models.Student.objects.create(stu_num=stu_num, stu_name=stu_name, stu_major=stu_major, stu_class=stu_class,
                                      abs_sum=0)

    student = models.Student.objects.order_by('stu_num')
    return render(request, "tec_manage.html",{'student':student},)

def tec_massage(request, nid):
    teacher = models.Teacher.objects.get(tec_num=nid)
    return render(request, "tec_massage.html", {'teacher':teacher})

def del_stu(request, nid):
    global student
    models.Student.objects.filter(pk=nid).delete()
    student = models.Student.objects.all()
    return render(request, "tec_manage.html", {'student':student})

global qr_time
def tec_sign(request):
    if request.method == 'GET':
        return render(request, "tec_sign.html")
    if request.method == 'POST':
        qr_time = request.POST.get("qr_time", None)
        print(qr_time)
        if qr_time:
            # print(request.user.username)
            sign_tec = tec_num
            # makeQrcode(request,qr_time,sign_tec)
            # 扫码签到，利用myqr包生成二维码并保存在文件中，如果文件中含有该二维码图片则不生成二维码
            # print(1)
            sign_begintime = timezone.now()
            print(sign_begintime)
            sign_finishtime = sign_begintime + datetime.timedelta(hours=int(qr_time))
            print(sign_finishtime)
            sign_con = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            print(sign_con)
            models.Signmanagement.objects.create(sign_con=sign_con, sign_tec=sign_tec, sign_begintime=sign_begintime,
                                                 sign_finishtime=sign_finishtime)
            sign = models.Signmanagement.objects.all()
            print(sign)
            try:
                # print(5)
                # url = request.GET.get('t')
                url = sign_con
                # url = 'www.baidu.com'
                # url = 'Sign in successfully!'
                # filename = "./static/" + str(base64.b64encode(str(url).encode('utf-8')), 'utf-8')+'.png'
                filename = str(base64.b64encode(str(url).encode('utf-8')), 'utf-8') + '.png'
                print("filename=" + str(filename))
                print(os.getcwd())
                # print(4)
                if os.path.exists(filename):
                    # print(3)
                    qrimg_data = open(filename, 'rb').read()
                    return HttpResponse(qrimg_data, content_type="image/png")
                    # return render(request, "tec_sign.html", {'filename': filename})
                    # print(3)
                else:
                    # print(2)
                    qr_name = myqr.run(
                        sign_con,
                        version=1,
                        level='H',
                        picture=None,
                        colorized=True,
                        contrast=1.0,
                        brightness=1.0,
                        save_name=filename,
                        save_dir=os.getcwd()
                    )
                    print(qr_name)
                    if os.path.exists(filename):
                        qrimg_data = open(filename, 'rb').read()
                        # return render(request, "tec_sign.html", {'filename': filename})
                        return HttpResponse(qrimg_data, content_type="image/png")
            except Exception as  e:
                return HttpResponse(str(e))

# 扫码签到，利用myqr包生成二维码并保存在文件中，如果文件中含有该二维码图片则不生成二维码
# def makeQrcode(request,qr_time,sign_tec):
#     print(1)
#     sign_begintime = timezone.now()
#     print(sign_begintime)
#     sign_finishtime = sign_begintime+ datetime.timedelta(hours= int(qr_time))
#     print(sign_finishtime)
#     sign_con = ''.join(random.sample(string.ascii_letters + string.digits, 8))
#     print(sign_con)
#     models.Signmanagement.objects.create(sign_con = sign_con,sign_tec=sign_tec,sign_begintime = sign_begintime,sign_finishtime=sign_finishtime)
#     sign = models.Signmanagement.objects.all()
#     print(sign)
#     try:
#         print(5)
#         # url = request.GET.get('t')
#         # url = sign_con
#         url = 'www.baidu.com'
#         # url = 'Sign in successfully!'
#         # filename = "./static/" + str(base64.b64encode(str(url).encode('utf-8')), 'utf-8')+'.png'
#         filename = str(base64.b64encode(str(url).encode('utf-8')), 'utf-8') + '.png'
#         print("filename=" + str(filename))
#         print(os.getcwd())
#         print(4)
#         if os.path.exists(filename):
#             print(3)
#             qrimg_data = open(filename, 'rb').read()
#             return HttpResponse(qrimg_data, content_type="image/png")
#             # return render(request, "tec_sign.html", {'filename': filename})
#             print(3)
#         else:
#             print(2)
#             qr_name = myqr.run(
#                 sign_con,
#                 version=1,
#                 level='H',
#                 picture=None,
#                 colorized=True,
#                 contrast=1.0,
#                 brightness=1.0,
#                 save_name=filename,
#                 save_dir='os.getcwd()'
#                 )
#             print(qr_name)
#             if os.path.exists(filename):
#                 qrimg_data = open(filename, 'rb').read()
#                 # return render(request, "tec_sign.html", {'filename': filename})
#                 return HttpResponse(qrimg_data, content_type="image/png")
#     except Exception as  e:
#         return HttpResponse(str(e))
