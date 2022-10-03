from django.urls import path
from .views import add_loopback_automation

urlpatterns = [
    path('addloopback', add_loopback_automation, name='store'),
    path('removeloopback', add_loopback_automation, name='store'),
]
