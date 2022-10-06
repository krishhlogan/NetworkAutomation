from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serrializer import DeviceConfigurationLogsSerializer
from rest_framework.decorators import api_view
from .tasks import add_loop_back, delete_loop_back
from .models import DeviceConfigurationLogs
from .managers.ConnectionManager import Connection, ConnectionManagerUtil
from collections import defaultdict


# Create your views here.
def validate_connection_config(connection: Connection):
    print(connection,type(connection))
    missing_keys = set(['device_type', 'host', 'username', 'password', 'loopbacks']) - set(connection.keys())
    print(missing_keys)
    if missing_keys:
        raise ValueError(f"Not all keys are not present in payload. Missing keys are {','.join(missing_keys)}")
    if not (connection['device_type'] and connection['host'] and connection['username'] and connection['password']):
        raise ValueError("Invalid Input data")


@api_view(["POST"])
def add_loopback_automation(request):
    try:
        map(validate_connection_config, request.data['devices'])
        if request.data['dry_run']:
            print("Starting dry run",request.data['devices'])
            commands = defaultdict(list)
            for device in request.data['devices']:
                for loopback in device['loopbacks']:
                    interface_config = f"""
                    interface loop {loopback["loopback_name"]}
                    description {loopback["description"]}
                    ip address {loopback["ipaddress"]} {loopback["subnet"]}
                    no shut
                    """
                    commands[device['host']].append(interface_config)
            return Response(status=200, data={"status": "success", "message": "dry run for adding loopback complete",
                                              "data": commands})
        else:
            add_loop_back.delay(request.data['devices'])
        return Response(status=200, data={"status": "success", "message": "adding loopback initiated successfully",
                                          "data": None})
    except ValueError as ve:
        return Response(status=400, data={"status": "fail", "exception": f"Error while adding loopback. {ve}"})
    except Exception as e:
        return Response(status=500, data={"status": "fail", "exception": f"Error while adding loopback. {e}"})


@api_view(["POST"])
def delete_loopback_automation(request):
    try:
        map(validate_connection_config, request.data['devices'])
        if request.data['dry_run']:
            commands = defaultdict(list)
            for device in request.data['devices']:
                for loopback in device['loopbacks']:
                    interface_config = f"no interface {loopback['interface_name']}"
                    commands[device['host']].append(interface_config)
            return Response(status=200, data={"status": "success", "message": "dry run for removing loopback complete",
                                              "data": commands})
        else:
            delete_loop_back.delay(request.data['devices'])
        return Response(status=200,
                        data={"status": "success", "message": "removing loopback initiated successfully", "data": None})
    except ValueError as ve:
        return Response(status=400, data={"status": "fail", "exception": f"Error while removing loopback. {ve}"})
    except Exception as e:
        return Response(status=500, data={"status": "fail", "exception": f"Error while removing loopback. {e}"})


@api_view(["POST"])
def list_interfaces(request):
    try:
        validate_connection_config(request.data)
        connectionManager = ConnectionManagerUtil(connection_config=request.data)
        interfaces, exception = connectionManager.list_interfaces()
        if exception is None:
            return Response(status=200, data={"status": "success", "data": interfaces})
        else:
            return Response(status=500, data={"status": "fail", "exception": exception})
    except Exception as e:
        return Response(status=500, data={"status": "fail", "exception": f"Error while getting interfaces. {e}"})


class ListLogs(ListAPIView):
    serializer_class = DeviceConfigurationLogsSerializer
    queryset = DeviceConfigurationLogs.objects.all().order_by('-created_at')
