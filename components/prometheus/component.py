from batou.component import Component
from batou.lib.archive import Extract
from batou.lib.download import Download
from batou.lib.file import File, Symlink
from batou_ext.nginx import VHost
from batou_ext.supervisor import Program
from batou_ext.user import User


class Prometheus(Component):

    version = '2.23.0'
    url = (
        'https://github.com/prometheus/prometheus/releases/download/'
        'v{version}/prometheus-{version}.linux-amd64.tar.gz')
    checksum = 'sha256:0f54cefdb946852947e35d4db8cfce394911ff586486f927c3887db4183cb643'

    def configure(self):
        self.url = self.url.format(version=self.version)

        self += User('prometheus')
        for name in ['bin', 'conf.d', 'data', 'node']:
            self += File('/srv/prometheus/%s' % name, ensure='directory',
                         owner='prometheus', group='prometheus')

        self += DownloadBinary(
            self.url.format(version=self.version), checksum=self.checksum,
            names=['prometheus', 'promtool'])
        self += Program(
            'prometheus',
            command='/srv/prometheus/bin/prometheus '
            '--config.file=/srv/prometheus/server.yml '
            '--storage.tsdb.path=/srv/prometheus/data '
            '--web.listen-address="127.0.0.1:9090" '
            # https://github.com/prometheus/prometheus/issues/1191
            '--web.external-url=https://pharos.wosc.de/prometheus/ '
            '--web.route-prefix=/',
            user='prometheus', dependencies=[self._])

        self += File('/srv/prometheus/server.yml', is_template=False)
        self.config = self._

        self += File('/srv/prometheus/nginx.conf', is_template=False)
        self += VHost(self._)

    def verify(self):
        self.config.assert_no_changes()

    def update(self):
        self.cmd('kill -HUP $(supervisorctl pid prometheus)')


class DownloadBinary(Component):

    namevar = 'url'
    checksum = None
    names = None

    def configure(self):
        self += Download(self.url, checksum=self.checksum)
        self += Extract(self._.target, strip=1, create_target_dir=False)
        for name in self.names:
            self += Symlink('/srv/prometheus/bin/%s' % name,
                            source=self.map(name))
