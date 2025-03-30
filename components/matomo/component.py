from batou import UpdateNeeded
from batou.component import Component
from batou.lib.download import Download
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.archive import Extract
from batou_ext.cron import CronJob
from batou_ext.mysql import ServiceDatabase
from batou_ext.nginx import VHost
from batou_ext.supervisor import PHP
from batou_ext.user import User, GroupMember


class Matomo(Component):

    version = '5.3.1'
    url = 'http://builds.matomo.org/matomo-{version}.tar.gz'
    # Since server sends `content-encoding` header, requests insists on already
    # unzipping. Thus, have to take the checksum from the .tar, not the .tar.gz!
    checksum = 'sha256:b753d5ebb262a324f02a4c6a172ecb798f99cd7fb722bbef9420a3da0ec28a44'

    packages = [
        'php8.3-cli',
        'php8.3-curl',
        'php8.3-gd',
        'php8.3-mbstring',
        'php8.3-mysql',
        'php8.3-xml',
        # 'php-geoip',
        # 'geoip-database-contrib',
    ]

    db_password = None
    ui_password = None

    import_logs = (
        '/srv/matomo/misc/log-analytics/import_logs.py '
        '--url https://pharos.wosc.de/logs/ --log-format-name=ncsa_extended '
        '--enable-http-errors --enable-http-redirects '
        '--enable-static --enable-bots '
        '--idsite={id} /var/log/nginx/{domain}-access.log.1 > /dev/null')

    def configure(self):
        for name in self.packages:
            self += Package(name)

        self += User('matomo')
        # Allow reading accesslogs
        self += GroupMember('adm', user='matomo')
        self += ServiceDatabase('matomo', password=self.db_password)

        self += File('/srv/matomo/setup/install.json',
                     owner='matomo', group='matomo', mode=0o640)
        self += Setup()

        self += Download(
            self.url.format(version=self.version), checksum=self.checksum,
            requests_kwargs={'headers': {'accept-encoding': '', 'accept': ''}})
        self += Extract(
            self._.target, target='/srv/matomo', strip=1,
            owner='matomo', group='matomo')

        self += PHP('matomo', user='matomo')

        self += File('/srv/matomo/nginx.conf', is_template=False)
        self += VHost(self._)

        self += CronJob(
            self.import_logs.format(id=1, domain='wosc.de'),
            user='matomo',
            timing='0 8 * * *')
        self += CronJob(
            self.import_logs.format(id=2, domain='grmusik.de'),
            user='matomo',
            timing='30 8 * * *')
        self += CronJob(
            'php /srv/matomo/console core:archive '
            '--url=https://pharos.wosc.de/logs/ > /dev/null',
            user='matomo',
            timing='0 9 * * *')

        self += File(
            '/etc/sudoers.d/matomo-geoip',
            content='matomo ALL=(root) NOPASSWD: /usr/sbin/update-geoip-database\n')
        # self += CronJob(
        #     'sudo update-geoip-database',
        #     user='matomo',
        #     timing='45 4 15 * *')


class Setup(Component):

    # https://github.com/nebev/piwik-cli-setup/pull/12
    url = (
        'https://github.com/jlebonzec/piwik-cli-setup/archive/'
        '85b13e8012e44cd0d6d66078b632222a7e4105df.tar.gz')
    checksum = 'sha256:9749aa4c15ffbb77041865c95d8b4f8ef537fbc3a16c0df4e9ef967c3194b049'

    def configure(self):
        self += Download(self.url, checksum=self.checksum)
        self += Extract(
            self._.target, target='/srv/matomo/setup', strip=1,
            owner='matomo', group='matomo')

    def verify(self):
        out, _ = self.cmd('echo "show tables" | mysql -uroot matomo')
        if not out.strip():
            raise UpdateNeeded()

    def update(self):
        self.cmd(
            'sudo -u matomo php /srv/matomo/setup/install.php')
