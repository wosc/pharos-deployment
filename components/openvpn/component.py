from batou.component import Component
from batou.lib.file import File, Directory
from batou_ext.apt import Package
from batou_ext.systemd import Service


class OpenVPN(Component):

    keys = {
        'ca': 'ca.crt',
        'cert': 'grmusik.de.crt',
        'key': 'grmusik.de.key',
        'tls_auth': 'ta.key',
    }
    # batou secrets
    ca = None
    cert = None
    key = None
    tls_auth = None

    def configure(self):
        self += File('/etc/sysctl.d/60-ipforward.conf',
                     content='net.ipv4.ip_forward=1')
        self += Service('systemd-sysctl', action='restart', deps=self._)

        self += Package('openvpn')
        package = self._

        config = []
        for source, target in self.keys.items():
            self += File(
                f'/etc/openvpn/server/{target}',
                content=getattr(self, source).replace(r'\n', '\n'),
                is_template=False, mode=0o600)
            config.append(self._)

        self += File('/etc/openvpn/server/grmusik.conf', source='server.conf')
        config.append(self._)
        self += Directory('/etc/openvpn/server/ccd')
        self += File(
            '/etc/openvpn/server/ccd/turawa',
            content='ifconfig-push 172.16.1.2 255.255.255.0')
        config.append(self._)

        self += Service(
            'openvpn-server@grmusik', action='restart', deps=config)
        self += Service(
            'openvpn-server@grmusik', action='enable', deps=package)
