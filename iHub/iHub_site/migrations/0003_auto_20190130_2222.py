# Generated by Django 2.1.5 on 2019-01-30 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iHub_site', '0002_plan_full'),
    ]

    operations = [
        migrations.RenameField(
            model_name='joinplan',
            old_name='have_ended',
            new_name='ended',
        ),
        migrations.AddField(
            model_name='joinplan',
            name='quitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='plan',
            name='canceled',
            field=models.BooleanField(default=False, verbose_name='是否已取消'),
        ),
    ]