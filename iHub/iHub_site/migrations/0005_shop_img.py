# Generated by Django 2.1.5 on 2019-02-20 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iHub_site', '0004_shop_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='img',
            field=models.ImageField(default='', upload_to='static/shop_img', verbose_name='商家展示'),
        ),
    ]
