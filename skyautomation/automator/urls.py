from django.urls import path
from .views import *

urlpatterns = [
    path('addLoopback', add_loopback_automation, name='add'),
    path('removeLoopback', delete_loopback_automation, name='remove'),
    path('listInterfaces',list_interfaces, name='list'),
    path('logs/', ListLogs.as_view(), name="list logs"),
]
