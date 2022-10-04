from rest_framework.serializers import ModelSerializer
from .models import DeviceConfigurationLogs


class DeviceConfigurationLogsSerializer(ModelSerializer):
    class Meta:
        model = DeviceConfigurationLogs
        fields = ('device', 'type', 'message', 'success', 'meta_data', 'created_at',)
