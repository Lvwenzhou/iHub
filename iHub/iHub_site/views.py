import datetime

from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from iHub_site.models import Users


def login(request):  # 登录
    if request.method == 'GET':
        return render(request, 'login.html')  # 需要一个登录页面(前端加油哇)

    if request.method == 'POST':
        user_no = request.POST.get('user_no')
        password = request.POST.get('password')
        # 使用auth模块在数据库中查询信息，验证用户是否存在，以验证用户名和密码
        user = auth.authenticate(username=user_no, password=password)
        # 这里的username指的是User表中的学号，在Django的auth_user表中的username使用学号
        # 我们的superuser也是在auth_user表中，superuser的is_staff字段是1，这些普通的用户is_staff字段为0
        auth.login(request, user)
        # 用于以后在调用每个视图函数前，auth中间件会根据每次访问视图前请求所带的SEESION里面的ID，去数据库找用户对像，并将对象保存在request.user属性中
        # 中间件执行完后，再执行视图函数
        if user:
            return redirect('/index/')  # 登录成功，返回至主页
        else:
            return render(request, 'login.html', {'wrong': True})  # 密码或用户名错误，反正没登陆成功
        # 这段登录的代码我也是借鉴的。反正就是用auth模块实现的登录
        # 验证是否登录用if request.user.is_authenticated
        # 所以可以通过request.user.username获取当前用户的学号/工号,然后根据学号/工号去User表中查询当前用户的各种信息
        # 这是我(shl)的写法……期待好一点的方式……


def register(request):  # 注册
    # 注册页面
    if request.method == 'GET':
        return render(request, 'register.html')
    # 提交注册
    if request.method == 'POST':
        name = request.POST.get('name_input')  # 输入姓名
        no = request.POST.get('no_input')  # 输入学号/工号
        username = request.POST.get('username_input')  # 输入用户名
        password = request.POST.get('password_input')  # 输入密码
        password_again = request.POST.get('password_again_input')  # 第二遍输入密码
        gender = request.POST.get('gender_select')  # 选择性别(前端选择框)
        wechatid = request.POST.get('wechatid_input')  # 微信ID,能够添加好友的方式
        reg_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 自动生成的注册时间
        mail = request.POST.get('mail_input')  # 输入邮箱
        major = request.POST.get('major_input')  # 输入专业
        credit = 100  # 默认100信誉积分
        # 还有头像……还不会做，先放着，以后再说

        if len(name) == 0 or len(no) == 0 or len(username) == 0 or len(password) == 0 or len(password_again) == 0 or len(gender) == 0 or len(mail) == 0 or len(wechatid) == 0 or len(major) == 0:
            return render(request, 'register.html', {'not_full': True})  # 填写信息不够完整,重来

        # 不允许一个学号/工号多次注册
        reg_tmp = Users.objects.filter(Q(no=no))
        if len(reg_tmp) != 0:
            return render(request, 'register.html', {'registered': True})  # 已注册过

        # 两次输入密码需一致
        if password == password_again:
            # 以下两句为创建Django的账户系统
            new_user = User.objects.create_user(username=no, password=password_again, email=mail)
            new_user.save()
            # 上述两句Django账户系统，使用用户学号/工号作为username
            password_md5 = make_password(password)  # MD5加密
            # 这里有个小问题……Django的账户系统有个库叫User,我们的账户系统起了个名叫Users……都用到了……比较像注意区分
            # 下面一句是向表User中添加一条数据
            Users.objects.create(username=username, no=no, gender=gender, name=name,
                                 password=password_md5, reg_time=reg_time, weChat_id=wechatid,
                                 mail=mail, major=major, credit=credit)
            return HttpResponseRedirect('/login/')  # 注册成功，跳转至登录界面
        else:
            return render(request, 'register.html', {'password_not_same': True})  # 两次密码输入不一致,重来


def logout(request):  # 登出
    if request.method == 'GET':
        # 以下一句为Django的账户系统
        auth.logout(request)
        response = HttpResponseRedirect('/index/')
        response.delete_cookie('ticket')
        return response

