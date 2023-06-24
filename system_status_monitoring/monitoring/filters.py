from django_filters import rest_framework as filters

from monitoring.models import SystemInfo

class UserInfoFilter(filters.FilterSet):
    # 时间过滤样式：&time=2022-12-02 00:00:00
    sort = filters.OrderingFilter(fields=['id',])
    class Meta:
        model=SystemInfo
        fields = {
            # 模糊查找，部分大小写
            'host_ip':['icontains'],
            # 大于，小于，年，月，周，日
            'time':['gte','lte','year','month','week','day'],
        }