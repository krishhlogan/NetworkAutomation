from django.urls import path
from .views import add_loopback_automation,delete_loopback_automation,get_logs

urlpatterns = [
    path('addloopback', add_loopback_automation, name='add'),
    path('removeloopback', delete_loopback_automation, name='remove'),
    path('logs',get_logs, name='logs')
]
