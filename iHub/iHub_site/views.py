import datetime

from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from iHub_site.models import Users, Plan, JoinPlan, Order, OrderFood, Shop, Menu


def login(request):  # 登录
    if request.method == 'GET':
        return render(request, 'login.html')  # 需要一个登录页面(前端加油哇)

    if request.method == 'POST':
        user_no = request.POST.get('user_no_input')
        password = request.POST.get('password_input')
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

        if len(name) == 0 or len(no) == 0 or len(username) == 0 or len(password) == 0 or len(
                password_again) == 0 or len(gender) == 0 or len(mail) == 0 or len(wechatid) == 0 or len(major) == 0:
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


# 以下是拼车相关功能的函数:

# 发起拼车
def start_plan(request):
    if request.method == 'GET':
        # 登录了才能发帖
        if not request.user.is_authenticated:
            return render(request, 'my.html', {'not_log_in': True})  # 未登录,跳转至个人主页去登录
        else:
            return render(request, 'start_plan.html')  # 已登录，跳转至发起拼车页面
    if request.method == 'POST':
        from_site = request.POST.get('from_site_input')  # 输入起始地点
        to_site = request.POST.get('to_site_input')  # 输入到达地点
        category = request.POST.get('category_input')  # 选择标签/分类
        trip_mode = request.POST.get('trip_mode_select')  # 选择出行方式
        deadline = request.POST.get('deadline_input')  # 输入截止时间
        trip_time = request.POST.get('trip_time_input')  # 输入计划出行时间
        note = request.POST.get('note_input')  # 输入备注
        num_need = request.POST.get('num_need_input')  # 输入除发起者外需要人数
        auth_gender = request.POST.get('auth_gender_input')  # 选择允许加入者性别(男性、女性、两者)
        pub_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 自动生成的发布时间

        user_no_now = request.user.username
        user_now = Users.objects.get(no=user_no_now)
        pub_username = user_now.username
        pub_name = user_now.name
        pub_no = user_now.no
        pub_wechat = user_now.weChat_id
        pub_gender = user_now.gender

        if len(from_site) == 0 or len(to_site) == 0 or len(trip_mode) == 0 or len(trip_time) == 0 or len(num_need) == 0:
            return render(request, 'start_plan.html', {'no_input': True})  # 未输入完整
        else:
            Plan.objects.create(from_site=from_site, to_site=to_site, category=category, trip_mode=trip_mode,
                                pub_time=pub_time, deadline=deadline, trip_time=trip_time, note=note, num_need=num_need,
                                auth_gender=auth_gender, pub_username=pub_username, pub_name=pub_name, pub_no=pub_no,
                                pub_wechat=pub_wechat, pub_gender=pub_gender)
            return HttpResponseRedirect('/plans/')  # 发起成功，返回查看拼车信息页面


# 加入拼车
def take_part(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:  # 若未登录
            plan_list = Plan.objects.filter(Q(ended=False) & Q(full=False))
            return render(request, 'plans.html', {'not_log_in': True, 'plan_list': plan_list})  # 返回查看拼车信息页面
        else:
            join_user_now = request.user.username
            join_user = Users.objects.get(no=join_user_now)

            join_plan_id = request.GET.get('plan_id')  # 返回参与事件在表Plan中的id
            join_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            join_no = join_user.no
            join_username = join_user.username
            join_name = join_user.name
            join_wechat = join_user.weChat_id
            join_gender = join_user.gender

            # 不可参加自己发起的事件
            plan_to_join = Plan.objects.get(id=join_plan_id)
            if plan_to_join.pub_no == join_user.no:
                plan_list = Plan.objects.filter(Q(ended=False) & Q(full=False))
                return render(request, 'plans.html', {'join_self': True, 'plan_list': plan_list})  # 返回查看拼车信息页面

            # 同一事件不可参加多次
            tmp = JoinPlan.objects.filter(Q(join_plan_id=join_plan_id) & Q(join_no=join_no))
            if len(tmp) != 0:
                plan_list = Plan.objects.filter(Q(ended=False) & Q(full=False))
                return render(request, 'plans.html', {'have_joined': True, 'plan_list': plan_list})  # 返回查看拼车信息页面

            JoinPlan.objects.create(join_no=join_no, join_username=join_username, join_name=join_name,
                                    join_wechat=join_wechat, join_gender=join_gender, join_plan_id=join_plan_id,
                                    join_time=join_time)

            plan_to_join.num_have = plan_to_join.num_have + 1  # 该事件参与人数加一
            plan_to_join.save()
            if plan_to_join.num_have == plan_to_join.num_need:  # 若该事件参与人数等于所需人数,full变为True,人数已满
                plan_to_join.full = True
                plan_to_join.save()

            return redirect('/my_plans/')  # 参与成功，返回个人信息页面


# 取消已发起的拼车事件
def cancel_plan(request):
    if request.method == 'GET':
        plan_id = request.GET.get('plan_id')  # 返回这一事件在Plan表中的id
        plan_to_cancel = Plan.objects.get(id=plan_id)
        plan_to_cancel.ended = True
        plan_to_cancel.canceled = True
        plan_to_cancel.save()
        related = JoinPlan.objects.filter(join_plan_id=plan_id)
        for item in related:  # 此处不知道对不对,PyCharm没给提示,还需测试
            item.canceled = True
            item.ended = True
            item.save()
        return redirect('/my_plans/')


# 退出已加入的拼车事件
def quit_plan(request):
    if request.method == 'GET':
        plan_id = request.GET.get('plan_id')  # 返回这一事件在Plan表中的id
        user_no = request.user.username

        plan_to_quit = Plan.objects.get(id=plan_id)
        plan_to_quit.num_have = plan_to_quit.num_have - 1
        plan_to_quit.save()
        if plan_to_quit.full:
            plan_to_quit.full = False
        plan_to_quit.save()

        related = JoinPlan.objects.get(Q(join_plan_id=plan_id) & Q(join_no=user_no))
        related.quitted = True
        related.save()

        return redirect('/my_plans/')


# 以下是早餐预定功能的函数：

# 进入早餐预定页面(学生端)
def order_bf(request):
    if request.method == 'GET':
        # 登录了才能进入页面
        if not request.user.is_authenticated:
            return render(request, 'my.html', {'not_log_in': True})  # 未登录,跳转至个人主页去登录
        else:
            return render(request, 'order_bf.html')  # 已登录，跳转至早餐预定页面


# 主页--按钮 进入主页 查看商家
def home(request):
    shop_list = Shop.objects.all()  # 获取所有商家数据
    return render(request, 'order_bf.html', {'shop_list', shop_list})  # 将商家数据渲染到页面上


# 我的--按钮
def my_orders(request):
    return render(request, 'my_orders.html')


# 选择商家后 显示菜单 并且 选择菜品支付
def menu_show(request):
    shop_id = request.GET.get('shop')  # 获取前端返回商家编号
    shop = Shop.objects.get(id=shop_id)
    if not shop.closed:  # 如果歇业时间大于当前时间
        Menu_list = Menu.objects.filter(shop=shop_id)  # 获取该商家编号的菜单
        return render(request, 'order_bf_menu.html', {'menu', Menu_list})  # 将菜单渲染到页面上
    else:  # 否则提示商家已歇业
        return


# 选择菜品
def food_chosen(request):
    goods_id = request.GET.get('goods_id')

