# Generated by Django 4.1.3 on 2022-11-22 15:37

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todonote',
            name='completed',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='todonote',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='todonote',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='todonote',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
