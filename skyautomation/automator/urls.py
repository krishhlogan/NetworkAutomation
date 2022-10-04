from django.urls import path
from .views import add_loopback_automation,delete_loopback_automation,get_logs,ListLogs

urlpatterns = [
    path('addloopback', add_loopback_automation, name='add'),
    path('removeloopback', delete_loopback_automation, name='remove'),
    path('logs/', ListLogs.as_view(), name="list logs"),
]
