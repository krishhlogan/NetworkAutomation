from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .managers.ConnectionManager import Connection, ConnectionManagerUtil


@shared_task
def add_loop_back(devices: list[Connection]):
    """
    Async function for adding a loopback
    Adds a loopback to device and stores the request in configuration logs

    Parameters:
    devices (list[Connection]): list of devices connections for which loopbacks are to be added

    Returns:
    Returns nothing
    """
    for connection_config in devices:
        connection = ConnectionManagerUtil(connection_config)
        connection.add_loopback()


@shared_task
def delete_loop_back(devices: list[Connection]):
    """
        Async function for removing a loopback
        Removes a loopback to device and stores the request in configuration logs

        Parameters:
        devices (list[Connection]): list of devices connections with interface names that need to be removed

        Returns:
        Returns nothing
        """
    for connection_config in devices:
        connection = ConnectionManagerUtil(connection_config)
        connection.remove_loopback()
