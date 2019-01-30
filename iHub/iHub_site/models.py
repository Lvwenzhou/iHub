from django.db import models


# Create your models here.
class Users(models.Model):  # 用户信息
    username = models.CharField(u"用户名", max_length=100)
    password = models.CharField(u"密码", max_length=100, null=True)  # 目前在Django的账户系统中存储密码,这里没必要存,可以为空
    no = models.CharField(u"学号/工号", max_length=100)
    name = models.CharField(u"姓名", max_length=100)
    gender = models.CharField(u"性别", max_length=100)
    major = models.CharField(u"专业", max_length=100)
    avatar = models.ImageField(upload_to="static/avatar", null=True)  # 头像这里还不会写，先让这里空着，基本功能做完再写
    mail = models.CharField(u"邮箱", max_length=100)
    weChat_id = models.CharField(u"微信ID", max_length=100)
    reg_time = models.DateTimeField(u"注册时间", max_length=100)
    credit = models.IntegerField(u"信誉积分", default=100)  # 信誉积分,默认100,取消拼车、退出拼车、预定不取会扣除


# 以下为预定早饭相关功能所需表
class Order(models.Model):  # 早饭预定订单，一个订单仅包括一个商家，多个商家需多个订单
    no = models.CharField(u"预定者学号/工号", max_length=100)
    order_time = models.DateTimeField(u"预定日期时间")
    get_time = models.DateTimeField(u"取早饭时间")
    ended = models.BooleanField(u"订单是否已结束", default=False)  # 默认为False，未结束
    shop = models.CharField(u"商家编号", max_length=100)  # 从哪一商家预定的，这一商家的编号
    note = models.CharField(u"备注", max_length=255)
    total = models.FloatField(u"总额")


class Menu(models.Model):  # 菜单(存放所有系统中有的菜品的表)
    name = models.CharField(u"菜品名称", max_length=100)
    img = models.ImageField(u"菜品缩略图", upload_to='static/menu_img')
    shop = models.CharField(u"商家编号", max_length=100)  # 来自哪一商家，这一商家的编号
    price = models.FloatField(u"单价")
    # 以下是否售罄、预定数量、初始数量，每日初始化或重新设置
    sell_out = models.BooleanField(u"是否售罄", default=False)  # 默认为False，未售罄
    ordered = models.IntegerField(u"以预定数量")
    initial = models.IntegerField(u"初始数量")


class Shop(models.Model):  # 商家
    name = models.CharField(u"商家名称", max_length=100)
    tel = models.CharField(u"联系电话", max_length=100)
    bus_hour = models.CharField(u"营业时间", max_length=100)  # 此处营业时间CharField。。让商家自己随便写吧。。
    note = models.CharField(u"商店说明", max_length=255)


class OrderFood(models.Model):  # 订单、菜品、商家之间的关系表
    # 这些id指的是表中的那列叫id的序号
    order_id = models.IntegerField(u"订单id")
    shop_id = models.IntegerField(u"商家id")
    goods_id = models.IntegerField(u"商品id")
    user_id = models.IntegerField(u"预定者id")
    num = models.IntegerField(u"商品数量")
    price = models.FloatField(u"商品单价")


# 以下是拼车相关功能所需表
class Plan(models.Model):  # 拼车计划
    from_site = models.CharField(u"起点", max_length=100)
    to_site = models.CharField(u"终点", max_length=100)
    category = models.CharField(u"标签/分类", max_length=100)
    trip_mode = models.CharField(u"出行方式", max_length=100)
    pub_time = models.DateTimeField(u"发布日期", auto_now=True)  # 该条计划发布时间
    deadline = models.DateTimeField(u"截止时间", null=True)  # 在此时间前加入
    trip_time = models.DateTimeField(u"计划出行时间")  # 计划出行时间
    pub_username = models.CharField(u"发布者昵称", max_length=100)
    pub_name = models.CharField(u"发布者姓名", max_length=100)
    pub_no = models.CharField(u"发布者学号/工号", max_length=100)
    pub_wechat = models.CharField(u"发布者微信ID", max_length=100)
    pub_gender = models.CharField(u"发布者性别", max_length=100)
    note = models.CharField(u"备注", max_length=255, null=True)
    num_need = models.IntegerField(u"需要人数")  # 除发起者外的需要人数
    num_have = models.IntegerField(u"已有人数", default=0)  # 默认已有0人
    full = models.BooleanField(u"是否人数已满", default=False)  # 默认False未满,当num_have==num_need时为True
    ended = models.BooleanField(u"是否已结束", default=False)  # 默认未结束(取消、已过出行时间、用户主动标记为结束,都算结束)
    canceled = models.BooleanField(u"是否已取消", default=False)  # 默认未取消(指用户主动取消此次行程)
    auth_gender = models.IntegerField(u"允许加入者性别")  # 0-均可加入,1-仅男性,2-仅女性

    def __unicode__(self):
        return self.id
    """
    class Meta:  # 按时间下降排序
        ordering = ['-pub_time']
        verbose_name = "出行计划"
        verbose_name_plural = "出行计划"
    """


class JoinPlan(models.Model):  # 参与者与计划的关系表
    join_no = models.CharField(u"参加者的学号/工号", max_length=100)
    join_username = models.CharField(u"参加者的昵称", max_length=100)
    join_name = models.CharField(u"参加者的姓名", max_length=100)
    join_wechat = models.CharField(u"参加者的微信ID", max_length=100)
    join_gender = models.CharField(u"参加者的性别", max_length=100)
    join_plan_id = models.IntegerField(u"所参加事件在Plan表中的序号")
    # 为了保证序号join_plan_id正确，Plan表中的数据不删除，可以改变ended的值来表示
    join_time = models.DateTimeField(auto_now=True)  # 加入时的时间
    ended = models.BooleanField(default=False)  # 计划结束(同Plan表中的ended) 默认False, 未结束
    canceled = models.BooleanField(default=False)  # 是否已取消(指行程是否已取消) 默认False, 未取消
    quitted = models.BooleanField(default=False)  # 是否已退出 默认False, 未退出
