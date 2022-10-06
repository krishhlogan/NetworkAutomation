from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .managers.ConnectionManager import Connection, ConnectionManagerUtil


@shared_task
def add_loop_back(devices: list[Connection]):
    for connection_config in devices:
        connection = ConnectionManagerUtil(connection_config)
        connection.add_loopback()
    return True


@shared_task
def delete_loop_back(devices: list[Connection]):
    for connection_config in devices:
        connection = ConnectionManagerUtil(connection_config)
        connection.remove_loopback()
    return True
