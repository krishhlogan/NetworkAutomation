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
    """
    Validates connection request

    Function validates the request for mandatory keys and values

    Parameters:
    connection (Connection): object of dataclass Connection used for connecting to device

    Returns:
    Nothing
    """
    missing_keys = set(['device_type', 'host', 'username', 'password', 'loopbacks']) - set(connection.keys())
    if missing_keys:
        raise ValueError(f"Not all keys are not present in payload. Missing keys are {','.join(missing_keys)}")
    if not (connection['device_type'] and connection['host'] and connection['username'] and connection['password']):
        raise ValueError("Invalid Input data")


@api_view(["POST"])
def add_loopback_automation(request):
    """
    View for adding loopback
    Function running the business logic to add loopbacks or return commands for adding loopback

    Parameter:
    request (HttpRequest): Accepts a django httpRequest, with data for dry_run and devices list in body

    Returns:
    Response: returns a Response object with status of request, exception message and data
    """
    try:
        map(validate_connection_config, request.data['devices'])
        if 'dry_run' in request.data and request.data['dry_run']:
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
    """
        View for deleting loopback
        Function running the business logic to remove loopbacks or return commands for removing loopback

        Parameter:
        request (HttpRequest): Accepts a django httpRequest, with data for dry_run and devices list in body

        Returns:
        Response: returns a Response object with status of request, exception message and data
        """
    try:
        map(validate_connection_config, request.data['devices'])
        if 'dry_run' in request.data and request.data['dry_run']:
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
    """
        View for adding loopback
        Function running the business logic to list interfaces

        Parameter:
        request (HttpRequest): Accepts a django httpRequest, with data for a single connection

        Returns:
        Response: returns a Response object with status of request, exception message and data
        """
    try:
        validate_connection_config(request.data)
        connection_manager = ConnectionManagerUtil(connection_config=request.data)
        interfaces, exception = connection_manager.list_interfaces()
        if exception is None:
            return Response(status=200, data={"status": "success", "data": interfaces})
        else:
            return Response(status=500, data={"status": "fail", "exception": exception})
    except Exception as e:
        return Response(status=500, data={"status": "fail", "exception": f"Error while getting interfaces. {e}"})


class ListLogs(ListAPIView):
    """
    ListAPIview for viewing logs of configuration request
    Used for listing all the device configuration requests received.
    """
    serializer_class = DeviceConfigurationLogsSerializer
    queryset = DeviceConfigurationLogs.objects.all().order_by('-created_at')
