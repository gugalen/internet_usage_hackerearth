from rest_framework import serializers
from internet.models import UsageData, AggSerializer

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageData
        fields = ('username', 'mac_address', 'start_time', 'usage_time', 'upload', 'download')

class MyAggSerializer(serializers.Serializer):
    time = serializers.DurationField()
    upload = serializers.DecimalField(max_digits=12, decimal_places=2)
    download = serializers.DecimalField(max_digits=12, decimal_places=2)