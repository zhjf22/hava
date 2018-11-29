from django.db import models

class SubmitInfo(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=100)
    user= models.CharField(max_length=100)
    password= models.CharField(max_length=100)
    hava_node= models.CharField(max_length=100)
    hava_user_group= models.CharField(max_length=100)
    hava_config= models.CharField(max_length=100)
    gmt_create = models.DateTimeField(auto_now=True)


class LogInfo(models.Model):
    log_id = models.IntegerField()
    log_context = models.CharField(max_length=1000)
    hava_submit_log_name = models.CharField(max_length=50,default='')
    hava_submit_log_pid = models.CharField(max_length=50,default='')
    states = models.CharField(max_length=50,default='')
    step = models.CharField(max_length=10,default='')
    gmt_create = models.DateTimeField(auto_now=True)


class Device(models.Model):
    host_name = models.CharField(primary_key=True,max_length=100)
    states = models.CharField(max_length=50)
    hava_user_group = models.CharField(max_length=100)
