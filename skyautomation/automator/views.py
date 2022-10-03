from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiTypes
from .tasks import add_loop_back

# Create your views here.


@extend_schema(request=OpenApiTypes.OBJECT, responses=OpenApiTypes.OBJECT)
@api_view(["POST"])
def add_loopback_automation(request):
    if "devices" not in request.data:
        raise ValueError("Device info not found")
    print(add_loop_back.delay(request.data["devices"]))
    return Response("hello world")
