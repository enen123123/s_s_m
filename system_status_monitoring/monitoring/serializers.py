from rest_framework import serializers
from monitoring.models import SystemInfo

class SystemSerializers(serializers.ModelSerializer):
    class Meta:
        model=SystemInfo
        fields = '__all__'


