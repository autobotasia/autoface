# Generated by Django 2.2.7 on 2020-04-13 06:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CameraList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_title', models.CharField(max_length=100)),
                ('area', models.CharField(max_length=100)),
                ('organization_name', models.CharField(max_length=100)),
                ('IP_camera', models.CharField(max_length=20)),
                ('status', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)])),
            ],
        ),
        migrations.CreateModel(
            name='GroupOfTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=30)),
                ('checkin', models.BooleanField(default=False)),
                ('checkin_time', models.TimeField()),
                ('checkout', models.BooleanField(default=False)),
                ('checkout_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=100)),
                ('admin', models.CharField(max_length=100)),
                ('location', models.TextField()),
                ('tel', models.CharField(max_length=15)),
            ],
        ),
    ]
