# Generated by Django 2.1.5 on 2019-01-28 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JoinPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_no', models.CharField(max_length=100, verbose_name='参加者的学号/工号')),
                ('join_username', models.CharField(max_length=100, verbose_name='参加者的昵称')),
                ('join_name', models.CharField(max_length=100, verbose_name='参加者的姓名')),
                ('join_wechat', models.CharField(max_length=100, verbose_name='参加者的微信ID')),
                ('join_gender', models.CharField(max_length=100, verbose_name='参加者的性别')),
                ('join_plan_id', models.IntegerField(verbose_name='所参加事件在Plan表中的序号')),
                ('join_time', models.DateTimeField(auto_now=True)),
                ('have_ended', models.BooleanField(default=False)),
                ('canceled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='菜品名称')),
                ('img', models.ImageField(upload_to='static/menu_img', verbose_name='菜品缩略图')),
                ('shop', models.CharField(max_length=100, verbose_name='商家编号')),
                ('price', models.FloatField(verbose_name='单价')),
                ('sell_out', models.BooleanField(default=False, verbose_name='是否售罄')),
                ('ordered', models.IntegerField(verbose_name='以预定数量')),
                ('initial', models.IntegerField(verbose_name='初始数量')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=100, verbose_name='预定者学号/工号')),
                ('order_time', models.DateTimeField(verbose_name='预定日期时间')),
                ('get_time', models.DateTimeField(verbose_name='取早饭时间')),
                ('ended', models.BooleanField(default=False, verbose_name='订单是否已结束')),
                ('shop', models.CharField(max_length=100, verbose_name='商家编号')),
                ('note', models.CharField(max_length=255, verbose_name='备注')),
                ('total', models.FloatField(verbose_name='总额')),
            ],
        ),
        migrations.CreateModel(
            name='OrderFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(verbose_name='订单id')),
                ('shop_id', models.IntegerField(verbose_name='商家id')),
                ('goods_id', models.IntegerField(verbose_name='商品id')),
                ('user_id', models.IntegerField(verbose_name='预定者id')),
                ('num', models.IntegerField(verbose_name='商品数量')),
                ('price', models.FloatField(verbose_name='商品单价')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_site', models.CharField(max_length=100, verbose_name='起点')),
                ('to_site', models.CharField(max_length=100, verbose_name='终点')),
                ('category', models.CharField(max_length=100, verbose_name='标签/分类')),
                ('trip_mode', models.CharField(max_length=100, verbose_name='出行方式')),
                ('pub_time', models.DateTimeField(auto_now=True, verbose_name='发布日期')),
                ('deadline', models.DateTimeField(null=True, verbose_name='截止时间')),
                ('trip_time', models.DateTimeField(verbose_name='计划出行时间')),
                ('pub_username', models.CharField(max_length=100, verbose_name='发布者昵称')),
                ('pub_name', models.CharField(max_length=100, verbose_name='发布者姓名')),
                ('pub_no', models.CharField(max_length=100, verbose_name='发布者学号/工号')),
                ('pub_wechat', models.CharField(max_length=100, verbose_name='发布者微信ID')),
                ('pub_gender', models.CharField(max_length=100, verbose_name='发布者性别')),
                ('note', models.CharField(max_length=255, null=True, verbose_name='备注')),
                ('num_need', models.IntegerField(verbose_name='需要人数')),
                ('num_have', models.IntegerField(default=0, verbose_name='已有人数')),
                ('ended', models.BooleanField(default=False, verbose_name='是否已结束')),
                ('auth_gender', models.IntegerField(verbose_name='允许加入者性别')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='商家名称')),
                ('tel', models.CharField(max_length=100, verbose_name='联系电话')),
                ('bus_hour', models.CharField(max_length=100, verbose_name='营业时间')),
                ('note', models.CharField(max_length=255, verbose_name='商店说明')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, verbose_name='用户名')),
                ('password', models.CharField(max_length=100, null=True, verbose_name='密码')),
                ('no', models.CharField(max_length=100, verbose_name='学号/工号')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('gender', models.CharField(max_length=100, verbose_name='性别')),
                ('major', models.CharField(max_length=100, verbose_name='专业')),
                ('avatar', models.ImageField(null=True, upload_to='static/avatar')),
                ('mail', models.CharField(max_length=100, verbose_name='邮箱')),
                ('weChat_id', models.CharField(max_length=100, verbose_name='微信ID')),
                ('reg_time', models.DateTimeField(max_length=100, verbose_name='注册时间')),
                ('credit', models.IntegerField(default=100, verbose_name='信誉积分')),
            ],
        ),
    ]
