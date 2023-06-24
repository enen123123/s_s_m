from django.db import models

# Create your models here.

class SystemInfo(models.Model):
    host_ip=models.CharField(max_length=40,verbose_name='主机ip',help_text='主机ip')
    cpu_usage=models.FloatField(max_length=20,verbose_name='CPU使用率',help_text='CPU使用率')
    menory_usage=models.FloatField(max_length=20,verbose_name='内存使用率',help_text='内存使用率')
    hardpan_usage=models.FloatField(max_length=20,verbose_name='硬盘使用率',help_text='硬盘使用率')
    # 网络io两个接口
    network_i=models.FloatField(max_length=40,verbose_name='网络I',help_text='网络I')
    network_o=models.FloatField(max_length=40,verbose_name='网络O',help_text='网络O')
    # 时间自动创建，年月日时分秒
    time=models.DateTimeField(max_length=20,verbose_name='日期时间',auto_now_add=True,help_text='日期时间')
