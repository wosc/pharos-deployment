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

    version = '4.0.4'
    url = 'http://builds.matomo.org/piwik-{version}.tar.gz'
    checksum = 'sha256:d4c1fc3487604d4a51247b1b5cbf84b2e2e855660f9874636aa3d673985bb3c3'

    packages = [
        'php7.2-cli',
        'php7.2-curl',
        'php7.2-gd',
        'php7.2-mbstring',
        'php7.2-mysql',
        'php7.2-xml',
        'php-geoip',
        'geoip-database-contrib',
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
            self.url.format(version=self.version), checksum=self.checksum)
        self += Extract(
            self._.target, target='/srv/matomo', strip=1,
            owner='matomo', group='matomo', create_target_dir=False)

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
        self += CronJob(
            'sudo update-geoip-database',
            user='matomo',
            timing='45 4 15 * *')


class Setup(Component):

    url = (
        'https://github.com/nebev/piwik-cli-setup/archive/'
        '63fcf3c428ccc1731f94875ac19a11a1640cd63c.tar.gz')
    checksum = 'sha256:916ab06f5880d4568b69ecf47195227f920071133ecdb1aa8fa975abb94e7b20'

    def configure(self):
        self += Download(self.url, checksum=self.checksum)
        self += Extract(
            self._.target, target='/srv/matomo/setup', strip=1,
            owner='matomo', group='matomo', create_target_dir=False)

    def verify(self):
        out, _ = self.cmd('echo "show tables" | mysql -uroot matomo')
        if not out.strip():
            raise UpdateNeeded()

    def update(self):
        self.cmd(
            'sudo -u matomo php /srv/matomo/setup/install.php')
