from rest_framework import serializers
from internet.models import UsageData

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageData
        fields = ('username', 'mac_address', 'start_time', 'usage_time', 'upload', 'download')
