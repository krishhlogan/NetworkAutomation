from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serrializer import DeviceConfigurationLogsSerializer
from rest_framework.decorators import api_view
from .tasks import add_loop_back, delete_loop_back
from .models import DeviceConfigurationLogs


# Create your views here.

@api_view(["POST"])
def add_loopback_automation(request):
    print(request.data)
    # if "devices" not in request.data:
    #     raise ValueError("Device info not found")
    print(add_loop_back.delay(request.data))
    return Response(status=200, data={"status": "success", "message": "adding loopback initiated successfully"})


@api_view(["POST"])
def delete_loopback_automation(request):
    # if "device_to_interface" not in request.data:
    #     raise ValueError("Device info not found")
    print(delete_loop_back.delay(request.data))
    return Response(status=200, data={"status": "success", "message": "deleting loopback initiated successfully"})


@api_view(["GET"])
def get_logs(request):
    print(DeviceConfigurationLogs.objects.all())
    op = [f.__dict__ for f in DeviceConfigurationLogs.objects.all()]
    print(op)
    return Response(data={"data":list(op)})


class ListLogs(ListAPIView):
    serializer_class = DeviceConfigurationLogsSerializer
    queryset = DeviceConfigurationLogs.objects.all()
