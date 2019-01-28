from django.db import models


# Create your models here.
class Users(models.Model):  # 用户信息
    username = models.CharField(u"用户名", max_length=100)
    password = models.CharField(u"密码", max_length=100)
    no = models.CharField(u"学号/工号", max_length=100)
    name = models.CharField(u"姓名", max_length=100)
    gender = models.CharField(u"性别", max_length=100)
    major = models.CharField(u"专业", max_length=100)
    avatar = models.ImageField(upload_to="static/avatar")
    mail = models.CharField(u"邮箱", max_length=100)
    weChat_id = models.CharField(u"微信ID", max_length=100)
    reg_time = models.DateTimeField(u"注册时间", max_length=100)


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
    order_id = models.CharField(u"订单id", max_length=100)
    shop_id = models.CharField(u"商家id", max_length=100)
    goods_id = models.CharField(u"商品id", max_length=100)
    user_id = models.CharField(u"预定者id", max_length=100)
    num = models.IntegerField(u"商品数量")
    price = models.FloatField(u"商品单价")
