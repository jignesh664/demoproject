# Generated by Django 3.0 on 2021-08-12 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20210806_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='area_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='myapp.Area'),
        ),
        migrations.AlterField(
            model_name='user',
            name='city_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='myapp.City'),
        ),
        migrations.AlterField(
            model_name='user',
            name='state_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='myapp.State'),
        ),
    ]
