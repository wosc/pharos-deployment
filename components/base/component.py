from batou.component import Component, Attribute
from batou.lib.archive import Extract
from batou.lib.download import Download
from batou.lib.file import File, Symlink
from batou_ext.apt import Package, AptRepository
from batou_ext.file import Delete
from batou_ext.nginx import VHost
from batou_ext.patch import Patch
from batou_ext.user import User, GroupMember

from batou_ext.cron import CronTab
from batou_ext.nginx import Nginx
from batou_ext.nodejs import NodeJS
from batou_ext.supervisor import Supervisor
from batou_ext.systemd import SystemdConfig


class BasePackages(Component):

    packages = Attribute('literal', """[
        'build-essential',
        'emacs-nox',
        'dnsutils',
        'git',
        'htop',
        'httpie',
        'jq',
        'mc',
        'mosh',
        'python3-dev',
        'python-is-python3',
        'rsync',
        'screen',
        'unzip',
        'zip',
    ]""")

    def configure(self):
        for name in self.packages:
            self += Package(name)

        # Allow accessing (mostly python) software installed by batou
        self += File('/root', ensure='directory', mode=0o755)

        self += User('wosc', home='/home/wosc')
        self += GroupMember('sudo', user='wosc')

        self += File('/etc/motd', is_template=False)


class CronAPT(Component):

    def configure(self):
        Delete('/etc/apt/apt.conf.d/20auto-upgrades')
        self += Package('cron-apt')
        self += File(
            '/etc/cron-apt/config', source='cron-apt.conf', is_template=False)


class MySQL(Component):

    packages = [
        'mysql-server-8.0',
        'mysql-client-8.0',
        'libmysqlclient-dev',
    ]

    def configure(self):
        for name in self.packages:
            self += Package(name)

        for name in ['backup', 'restore']:
            self += File('/usr/local/bin/mysql-%s' % name,
                         is_template=False, mode=0o755)
        self += Symlink('/etc/cron.daily/mysql-backup',
                        source='/usr/local/bin/mysql-backup')


class PHPBase(Component):

    version = '7.4'

    def configure(self):
        self += Package('php%s' % self.version)
        self += Package('php%s-cgi' % self.version)
        # Send php errors to nginx log.
        self += Patch(
            '/etc/php/%s/cgi/php.ini' % self.version,
            source=';error_log = php_errors.log',
            target='error_log = /dev/stderr')


class Pharos(Component):

    def configure(self):
        self += File('/etc/nginx/sites-available/pharos.wosc.de',
                     source='pharos.conf', is_template=False)
        self += VHost(self._, site_enable=True)


class Jamulus(Component):

    def configure(self):
        self += File(
            '/etc/systemd/system/jamulus-headless.service.d'
            '/jamulus-headless.conf', leading=True, is_template=False)
        self += AptRepository(
            'jamulus',
            line='deb http://ppa.launchpad.net/tormodvolden/jam/ubuntu xenial main',
            key='https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x627abb1e29cc8356ad0800eb4b1e287796dd5c9a')
        self += Package('jamulus')


class Soundjack(Component):

    version = '210106'

    packages = [
        'libjack-jackd2-0',
        'libqt5core5a',
        'libqt5gui5',
        'libqt5multimediawidgets5',
        'libqt5websockets5',
        'libqt5widgets5',
        'xvfb',
    ]

    url = 'https://www.soundjack.eu/Downloads/SJC{version}.tar.gz'
    checksum = 'sha256:eff6f938b435b24299918d542b7b91bdacd0247460e20046cd35d710dd240500'

    def configure(self):
        for name in self.packages:
            self += Package(name)

        self += Download(
            self.url.format(version=self.version), checksum=self.checksum)
        self += Extract(self._.target, strip=2, create_target_dir=False)
        self += Symlink('/usr/local/bin/soundjack',
                        source=self.map('SJC%s' % self.version))

        self += File(
            '/lib/systemd/system/soundjack.service',
            source='soundjack.conf', is_template=False)
        self += SystemdConfig(self._)
