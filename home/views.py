import datetime
from xmlrpc.client import DateTime

from django.shortcuts import render
from django.contrib import messages
from . import models
from django.http import HttpResponse

from django.utils import timezone #引入timezone模块
# Create your views here.
stu_num = '170101'
stu_password = '000'
sign_con = 'abcdefg'

def index(request):
    global stu_num,stu_password
    if request.method == "POST":
        stu_num = request.POST.get("stu_num", None)
        stu_password = request.POST.get("password", None)
        student = models.Student.objects.filter(stu_num=stu_num)
        if student.exists() and stu_password == models.Student.objects.get(stu_num=stu_num).stu_password:
            return render(request,'stu_check.html', {'student':models.Student.objects.get(stu_num=stu_num)})
        else:
            messages.success(request, "账号或密码有误，请重新登录")
            return render(request, 'index.html')
    else:
        return render(request, "index.html")

def stu_check(request):
    return render(request, 'stu_check.html')


def stu_sign(request,nid):
    global sign_con
    if request.method == "GET":
        return render(request, 'stu_sign.html',{'stu_num':nid})
    if request.method == "POST":
        sign_con = request.POST.get("sign_con", None)
    print(sign_con)
    sign = models.Signmanagement.objects.filter(sign_con=sign_con)
    print(sign)
    sign_time = timezone.now()
    print(sign_time)
    if sign.exists() :
        # if DateTime.Compare(sign_time, sign.sign_begintime) != -1 and  DateTime.Compare(sign_time, sign.sign_finishtime) != 1:
        # if sign_time >= datetime.datetime.strptime(models.Signmanagement.objects.get(sign_con=sign_con).sign_begintime,'%Y-%m-%d %H:%M:%S' ) and sign_time <= datetime.datetime.strptime(models.Signmanagement.objects.get(sign_con=sign_con).sign_finishtime,'%Y-%m-%d %H:%M:%S' ):
        sign_time = sign_time.strftime("%Y-%m-%d %H:%M:%S")
        if sign_time >= models.Signmanagement.objects.get(sign_con=sign_con).sign_begintime and sign_time <= models.Signmanagement.objects.get(sign_con=sign_con).sign_finishtime:
            student = models.Student.objects.get(stu_num=nid)
            # student.abs_num = student.abs_num+1
            print(student)
            if student.stu_con == sign_con:
                messages.success(request, "不可重复签到")
                return render(request, 'stu_sign.html', {'stu_num': nid})
            else :
                student.stu_con = sign_con
                messages.success(request, "签到成功")
                student.save()
                sign_time = datetime.datetime.strptime(sign_time, '%Y-%m-%d %H:%M:%S')
                sign_time = sign_time + datetime.timedelta(hours=8)
                return render(request, 'stu_acc.html', {'stu_time': sign_time})
        else:
            messages.success(request, "请在签到时间内签到")
            return render(request, 'stu_sign.html',{'stu_num':nid})
    else:
         messages.success(request, "请输入二维码信息")
    return render(request, 'stu_sign.html',{'stu_num':nid})

def stu_acc(request):
    return render(request, 'stu_acc.html')
