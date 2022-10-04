from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .managers.ConnectionManager import Connection, ConnectionManagerUtil


def validate_connection_config(connection: Connection, request_type: str):
    if not (connection['device_type'] and connection['host'] and connection['username'] and connection['password'] and
            connection['loopbacks']):
        raise ValueError("Invalid Input data")


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
