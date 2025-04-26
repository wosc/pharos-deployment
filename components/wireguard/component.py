from batou.component import Component
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.systemd import Service


class Wireguard(Component):

    key_server_private = None
    key_server_public = None
    key_client_private = None
    key_client_public = None

    def configure(self):
        self += File('/etc/sysctl.d/60-ipforward.conf',
                     content='net.ipv4.ip_forward=1')
        self += Service('systemd-sysctl', action='restart', deps=self._)

        self += Package('wireguard')
        package = self._

        self += File('/etc/wireguard/wg0.conf', source='server.conf')
        config = self._
        self += File('/etc/wireguard/client.conf', source='client.conf')

        self += Service('wg-quick@wg0', action='restart', deps=config)
        self += Service('wg-quick@wg0', action='enable', deps=package)

