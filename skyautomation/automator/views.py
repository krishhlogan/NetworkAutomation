from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serrializer import DeviceConfigurationLogsSerializer
from rest_framework.decorators import api_view
from .tasks import add_loop_back, delete_loop_back
from .models import DeviceConfigurationLogs


# Create your views here.

@api_view(["POST"])
def add_loopback_automation(request):
    try:
        add_loop_back.delay(request.data)
        return Response(status=200, data={"status": "success", "message": "adding loopback initiated successfully"})
    except ValueError as ve:
        return Response(status=400, data={"status": "fail", "message": f"Error while adding loopback. {ve}"})
    except Exception as e:
        return Response(status=500, data={"status" : "fail", "message": f"Error while adding loopback. {e}"})


@api_view(["POST"])
def delete_loopback_automation(request):
    try:
        delete_loop_back.delay(request.data)
        return Response(status=200, data={"status": "success", "message": "removing loopback initiated successfully"})
    except ValueError as ve:
        return Response(status=400, data={"status": "fail", "message": f"Error while removing loopback. {ve}"})
    except Exception as e:
        return Response(status=500, data={"status" : "fail", "message": f"Error while removing loopback. {e}"})


class ListLogs(ListAPIView):
    serializer_class = DeviceConfigurationLogsSerializer
    queryset = DeviceConfigurationLogs.objects.all().order_by('-created_at')
    # ordering = ['-created_at']
