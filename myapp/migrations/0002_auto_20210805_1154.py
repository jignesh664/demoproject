# Generated by Django 3.0 on 2021-08-05 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='state_id',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=100)),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.State')),
            ],
        ),
    ]
