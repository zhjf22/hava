# Generated by Django 2.1.2 on 2018-12-01 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('havaApp', '0003_loginfo_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginfo',
            name='host_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
