# Generated by Django 4.1.3 on 2022-11-22 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_alter_todonote_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='todonote',
            name='category',
            field=models.CharField(choices=[('d', 'daily'), ('w', 'weekly'), ('m', 'monthly'), ('q', 'quarterly'), ('y', 'yearly')], default='d', max_length=20),
        ),
    ]