from batou.component import Component
from batou.lib.archive import Extract
from batou.lib.download import Download
from batou.lib.file import File, Symlink
from batou_ext.cron import CronJob
from batou_ext.nginx import VHost
from batou_ext.python import VirtualEnv, Requirements
from batou_ext.supervisor import Program
from batou_ext.user import User, GroupMember
from glob import glob
import batou.lib.mysql
import os


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
        self.config = [self._] + self.require('prom:rule', host=self.host)

        self += File('/srv/prometheus/nginx.conf', is_template=False)
        self += VHost(self._)

    def verify(self):
        for dep in self.config:
            dep.assert_no_changes()

    def update(self):
        self.cmd('kill -HUP $(supervisorctl pid prometheus)')


class Prom_Node(Component):

    version = '1.0.1'
    url = (
        'https://github.com/prometheus/node_exporter/releases/download/'
        'v{version}/node_exporter-{version}.linux-amd64.tar.gz')
    checksum = 'sha256:3369b76cd2b0ba678b6d618deab320e565c3d93ccb5c2a0d5db51a53857768ae'

    def configure(self):
        self += DownloadBinary(
            self.url.format(version=self.version), checksum=self.checksum,
            names=['node_exporter'])
        self += Program(
            'prometheus-node',
            command='/srv/prometheus/bin/node_exporter '
            '--collector.textfile.directory=/srv/prometheus/node '
            '--web.listen-address="127.0.0.1:9100"',
            user='prometheus', dependencies=[self._])

        # node_exporter doesn't expose total number of processes, unsure if
        # <https://github.com/prometheus/node_exporter/issues/790> will help.
        self += File('/srv/prometheus/bin/node_exporter-numprocs',
                     source='numprocs.sh', is_template=False, mode=0o755)
        self += CronJob(
            '/srv/prometheus/bin/node_exporter-numprocs',
            user='prometheus',
            timing='* * * * *')


class Prom_Push(Component):

    version = '1.3.1'
    url = (
        'https://github.com/prometheus/pushgateway/releases/download/'
        'v{version}/pushgateway-{version}.linux-amd64.tar.gz')
    checksum = 'sha256:374055d60648961f4defe0f08c392f8bc0c9c17856a0e9ec34a063e35a6dec48'

    def configure(self):
        self += DownloadBinary(
            self.url.format(version=self.version), checksum=self.checksum,
            names=['pushgateway'])
        self += Program(
            'prometheus-node',
            command='/srv/prometheus/bin/pushgateway',
            user='prometheus', dependencies=[self._])


class Prom_Alert(Component):

    version = '0.21.0'
    url = (
        'https://github.com/prometheus/alertmanager/releases/download/'
        'v{version}/alertmanager-{version}.linux-amd64.tar.gz')
    checksum = 'sha256:9ccd863937436fd6bfe650e22521a7f2e6a727540988eef515dde208f9aef232'

    pushover_user_key = None
    pushover_api_key = None

    def configure(self):
        self += File('/srv/prometheus/data/alerts', ensure='directory',
                     owner='prometheus', group='prometheus')

        self += DownloadBinary(
            self.url.format(version=self.version), checksum=self.checksum,
            names=['alertmanager', 'amtool'])
        self += Program(
            'prometheus-alert',
            command='/srv/prometheus/bin/alertmanager '
            '--config.file=/srv/prometheus/alert.yml '
            '--storage.path=/srv/prometheus/data/alerts '
            '--cluster.listen-address="127.0.0.1:9094" '
            '--cluster.advertise-address="127.0.0.1:19094" '
            '--web.listen-address="127.0.0.1:9093" '
            '--web.external-url=https://pharos.wosc.de/prometheus-alert/ '
            '--web.route-prefix=/',
            user='prometheus', dependencies=[self._])

        self += File('/srv/prometheus/alert.yml')
        self.config = self._

        self += File(
            '/srv/prometheus/bin/send-alert',
            source='send-alert.sh', is_template=False, mode=0o755)

    def verify(self):
        self.config.assert_no_changes()

    def update(self):
        self.cmd('kill -HUP $(supervisorctl pid prometheus-alert)')


class Prom_Exim(Component):

    email_password = None

    def configure(self):
        # Allow running `mailq`
        self += GroupMember('Debian-exim', user='prometheus')
        self += File('/srv/prometheus/bin/node_exporter-mailq',
                     source='mailq.sh', is_template=False, mode=0o755)
        self += CronJob(
            '/srv/prometheus/bin/node_exporter-mailq',
            user='prometheus',
            timing='* * * * *')

        # Allow reading exim mainlog
        self += GroupMember('adm', user='prometheus')
        self += File('/srv/prometheus/bin/node_exporter-eximstats',
                     source='eximstats.sh', is_template=False, mode=0o755)
        self += CronJob(
            '/srv/prometheus/bin/node_exporter-eximstats',
            user='prometheus',
            timing='*/5 * * * *')

        self += VirtualEnv()
        self._ += Requirements(source='mailcheck.txt')

        self += File('/srv/prometheus/mailcheck.conf',
                     owner='prometheus', group='prometheus', mode=0o640)
        self += File('/srv/prometheus/caldavcheck.conf',
                     owner='prometheus', group='prometheus', mode=0o640)

        self += File('/srv/prometheus/bin/node_exporter-mailcheck',
                     source='mailcheck.sh', is_template=False, mode=0o755)
        self += CronJob(
            '/srv/prometheus/bin/node_exporter-mailcheck',
            user='prometheus',
            timing='*/5 * * * *')

        self += File(
            '/srv/prometheus/conf.d/alert-mailcheck.yml', is_template=False)
        self.provide('prom:rule', self._)


class Prom_Github(Component):

    api_key = None
    owner = 'wosc'

    def configure(self):
        self += VirtualEnv()
        self._ += Requirements(source='github.txt')

        self += Program(
            'prometheus-github',
            command=self.map('bin/github_vulnerability_exporter') +
            ' --host=127.0.0.1 --port=9597 --ttl=3590',
            environ='GITHUB_AUTHTOKEN="%s", GITHUB_OWNER="%s"' % (
                self.api_key, self.owner),
            user='prometheus', dependencies=[])

        self += File(
            '/srv/prometheus/conf.d/alert-github.yml', is_template=False)
        self.provide('prom:rule', self._)


class Prom_Mysql(Component):

    version = '0.12.1'
    url = (
        'https://github.com/prometheus/mysqld_exporter/releases/download/'
        'v{version}/mysqld_exporter-{version}.linux-amd64.tar.gz')
    checksum = 'sha256:133b0c281e5c6f8a34076b69ade64ab6cac7298507d35b96808234c4aa26b351'

    db_password = None

    def configure(self):
        self += batou.lib.mysql.User('prometheus', password=self.db_password)
        self += batou.lib.mysql.Command(admin_password=None, statement=(
            "GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* "
            "TO 'prometheus'@'localhost';"))

        self += DownloadBinary(
            self.url.format(version=self.version), checksum=self.checksum,
            names=['mysqld_exporter'])
        self += Program(
            'prometheus-mysql',
            command='/srv/prometheus/bin/mysqld_exporter '
            '--web.listen-address="127.0.0.1:9104"',
            environ='DATA_SOURCE_NAME="prometheus:%s@(localhost:3306)/"' % (
                self.db_password),
            user='prometheus', dependencies=[self._])


class Prom_Nginx(Component):

    version = '1.2.0'
    url = (
        'https://github.com/martin-helmich/prometheus-nginxlog-exporter'
        '/releases/download/v{version}/prometheus-nginxlog-exporter')
    checksum = 'sha256:ef9ea0acaac70c1e9e15408375fb0440bf01cfd744e0b8f3e57c8526dc405f01'

    def configure(self):
        # Allow reading accesslogs
        self += GroupMember('adm', user='prometheus')
        self += Download(
            self.url.format(version=self.version), checksum=self.checksum)
        self.download = self._
        self += Symlink(
            '/srv/prometheus/bin/nginx_exporter', source=self._.target)

        self.logfiles = glob('/var/log/nginx/*-access.log')
        self += File('/srv/prometheus/nginx.yml')
        self += Program(
            'prometheus-nginx',
            command='/srv/prometheus/bin/nginx_exporter '
            '-config-file /srv/prometheus/nginx.yml',
            user='prometheus', dependencies=[self._])

    def verify(self):
        self.download.assert_no_changes()

    def update(self):
        os.chmod(self.download.target, 0o755)
