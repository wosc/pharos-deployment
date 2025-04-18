from batou.component import Component
from batou.lib.file import File
from batou_ext.apt import AptRepository, Package
from batou_ext.mysql import ServiceDatabase
from batou_ext.nginx import VHost
from batou_ext.systemd import Service


class Grafana(Component):

    db_password = None
    ui_password = None

    def configure(self):
        self += ServiceDatabase('grafana', password=self.db_password)

        self += Package('apt-transport-https')
        self += AptRepository(
            'grafana',
            url='https://apt.grafana.com/',
            distro='stable',
            key='https://apt.grafana.com/gpg-full.key')
        self += Package('grafana')

        self += File('/etc/grafana/grafana.ini')
        self += Service('grafana-server', action='restart', deps=self._)

        self += File(
            '/srv/prometheus/grafana-nginx.conf',
            source='nginx.conf', is_template=False)
        self += VHost(self._)

        # Manually add Prometheus data source:
        # http://localhost:9090/, proxy through grafana
