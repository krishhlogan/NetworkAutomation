import netmiko
from netmiko import NetMikoTimeoutException
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
    action: Literal['ADD', 'REMOVE']
    loopbacks: List[Loopback]
    secret: str = ""
    port: int = 22


class ConnectionManagerUtil:
    def __init__(self, connection_config: Connection):
        self.connection_config = connection_config

    def get_connection(self):
        if True:
            device_config = {
                'device_type': self.connection_config['device_type'],
                'host': self.connection_config['host'],
                'username': self.connection_config['username'],
                'password': self.connection_config['password'],
                'port': self.connection_config['port'],  # optional, defaults to 22
                'secret': self.connection_config['secret']  # optional, defaults to ''
            }
            print("logging config ", device_config)
            return netmiko.ConnectHandler(**device_config)
        # except (EOFError, SSHException, NetMikoTimeoutException):
        #     print(f"SSH is not enabled for the device: {self.connection_config['host']}")

    def add_loopback(self):
        print(self.connection_config["loopbacks"])
        for loopback in self.connection_config["loopbacks"]:
            print(loopback)
            connection = self.get_connection()
            interface_config = [
                "interface loop {}".format(loopback["loopback_name"]),
                "description {}".format(loopback["description"]),
                "ip address {} {}".format(loopback["ipaddress"], loopback["subnet"]),
                "no shut"
            ]
            output = connection.send_config_set(interface_config)
            log = DeviceConfigurationLogs(
                device = self.connection_config["host"]+'_'+self.connection_config['device_type'],
                message = output,
                success = False if 'invalid' in output.lower() else True,
                meta_data = self.connection_config
            )
            print(log)
            log.save()
            print(DeviceConfigurationLogs.objects.all())
            print(output)

    def remove_loopback(self):
        for loopback in self.connection_config["loopbacks"]:
            print(loopback)
            connection = self.get_connection()
            interface_config = [
                "no interface {}".format(loopback["interface_name"])
            ]
            output = connection.send_config_set(interface_config)
            log = DeviceConfigurationLogs(
                device=self.connection_config["host"] + '_' + self.connection_config['device_type'],
                message=output,
                success=False if 'invalid' in output.lower() else True,
                meta_data=self.connection_config
            )
            log.save()

