# Generated by Django 2.1.2 on 2018-12-02 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('havaApp', '0005_record'),
    ]

    operations = [
        migrations.CreateModel(
            name='HavaUserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_group', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Record',
        ),
    ]