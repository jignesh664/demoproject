# Generated by Django 3.0 on 2021-08-13 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20210812_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='is_deleted',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='city',
            name='is_deleted',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='state',
            name='is_deleted',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='is_deleted',
            field=models.IntegerField(default=1),
        ),
    ]
