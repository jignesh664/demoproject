# Generated by Django 3.0 on 2021-08-14 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20210813_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='is_active',
            field=models.IntegerField(default='inactive'),
        ),
        migrations.AlterField(
            model_name='city',
            name='is_active',
            field=models.IntegerField(default='inactive'),
        ),
        migrations.AlterField(
            model_name='state',
            name='is_active',
            field=models.IntegerField(default='inactive'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.IntegerField(default='inactive'),
        ),
    ]