import netmiko
from netmiko import NetMikoTimeoutException, NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
from dataclasses import dataclass
from typing import Literal, List
from ..models import DeviceConfigurationLogs


@dataclass
class Loopback:
    loopback_name: int
    interface_name: str = ""
    description: str = ""
    ipaddress: str = ""
    subnet: str = ""


@dataclass
class Connection:
    device_type: str
    host: str
    username: str
    password: str
    action: Literal['ADD', 'REMOVE', 'LIST']
    loopbacks: List[Loopback]
    secret: str = ""
    port: int = 22


class ConnectionManagerUtil:
    def __init__(self, connection_config: Connection):
        """
        Constructor to set up connection config details
        """
        self.connection_config = connection_config

    def get_connection(self):
        """
        Method to connect to the device using the connection config
        """
        try:
            device_config = {
                'device_type': self.connection_config['device_type'],
                'host': self.connection_config['host'],
                'username': self.connection_config['username'],
                'password': self.connection_config['password'],
                'port': self.connection_config['port'],  # optional, defaults to 22
                'secret': self.connection_config['secret']  # optional, defaults to ''
            }
            return netmiko.ConnectHandler(**device_config), None
        except NetMikoTimeoutException as nte:
            message = f"Unable to reach device. NetMikoTimeoutException while connecting to device. {nte}"
            return None, message
        except SSHException as se:
            message = f"ssh failure. SSHException while connecting to device. {se}"
            return None, message
        except NetmikoAuthenticationException as nae:
            message = f"Auth failure. NetmikoAuthenticationException while connecting to device. {nae}"
            return None, message
        except Exception as e:
            message = f"Exception while connecting to device. {e}"
            return None, message

    def list_interfaces(self):
        """
        Method for listing interfaces for given connection config
        """
        connection, exception = self.get_connection()
        if connection is not None:
            interfaces = connection.send_command('show ip int brief', use_textfsm=True)
            DeviceConfigurationLogs.objects.create(
                device=self.connection_config["host"] + '_' + self.connection_config['device_type'],
                type='LIST',
                message=interfaces,
                success=True,
                meta_data=self.connection_config
            )
            return interfaces, exception
        else:
            DeviceConfigurationLogs.objects.create(
                device=self.connection_config["host"] + '_' + self.connection_config['device_type'],
                type='LIST',
                message=exception,
                success=False,
                meta_data=self.connection_config
            )
            return None, exception

    def add_loopback(self):
        """
        Method for adding loopbacks to given connection
        """
        for loopback in self.connection_config["loopbacks"]:
            connection, exception = self.get_connection()
            if connection is not None:
                interface_config = [
                    "interface loop {}".format(loopback["loopback_name"]),
                    "description {}".format(loopback["description"]),
                    "ip address {} {}".format(loopback["ipaddress"], loopback["subnet"]),
                    "no shut"
                ]
                output = connection.send_config_set(interface_config)
                connection.cleanup()
                DeviceConfigurationLogs.objects.create(
                    device=self.connection_config["host"] + '_' + self.connection_config['device_type'],
                    type='ADD',
                    message=output,
                    success=False if 'invalid' in output.lower() else True,
                    meta_data=self.connection_config
                )
            else:
                DeviceConfigurationLogs.objects.create(
                    device=self.connection_config["host"] + '_' + self.connection_config['device_type'],
                    type='ADD',
                    message=exception,
                    success=False,
                    meta_data=self.connection_config
                )
                raise Exception(exception)

    def remove_loopback(self):
        """
        Method for removing loopbacks for a given connection
        """
        for loopback in self.connection_config["loopbacks"]:
            connection, exception = self.get_connection()
            if connection is not None:
                interface_config = [
                    "no interface {}".format(loopback["interface_name"])
                ]
                output = connection.send_config_set(interface_config)
                connection.cleanup()
                DeviceConfigurationLogs.objects.create(
                    device=self.connection_config["host"] + '_' + self.connection_config['device_type'],
                    type='REMOVE',
                    message=output,
                    success=False if 'invalid' in output.lower() else True,
                    meta_data=self.connection_config
                )
            else:
                DeviceConfigurationLogs.objects.create(
                    device=self.connection_config["host"] + '_' + self.connection_config['device_type'],
                    type='ADD',
                    message=exception,
                    success=False,
                    meta_data=self.connection_config
                )
                raise Exception(exception)
